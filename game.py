from collections import OrderedDict
import save_game_manager
import stats_manager
import tetriminos
import settings
import logging
import helpers
import random
import pygame
import time
import sys
import os


class Game:
    save_data = [
        'fallen_blocks',
        'level',
        'lines',
        'score',
        'duration',
        'current_tetrimino',
        'next_tetrimino'
    ]

    infos = [
        {'name': 'Level', 'value': 'level', 'format': helpers.humanize_integer},
        {'name': 'Lines', 'value': 'lines', 'format': helpers.humanize_integer},
        {'name': 'Score', 'value': 'score', 'format': helpers.humanize_integer},
        {'name': 'Time', 'value': 'duration', 'format': helpers.humanize_seconds}
    ]

    stats = OrderedDict([
        ('play_time', {'name': 'Play time', 'value': 0, 'format': helpers.humanize_seconds}),
        ('longest_game', {'name': 'Longest game', 'value': 0, 'format': helpers.humanize_seconds}),
        ('games_played', {'name': 'Total games played', 'value': 0, 'format': helpers.humanize_integer}),
        ('overall_score', {'name': 'Overall score', 'value': 0, 'format': helpers.humanize_integer}),
        ('overall_lines', {'name': 'Overall lines', 'value': 0, 'format': helpers.humanize_integer}),
        ('max_score', {'name': 'Maximum score', 'value': 0, 'format': helpers.humanize_integer}),
        ('max_lines', {'name': 'Maximum lines', 'value': 0, 'format': helpers.humanize_integer}),
        ('max_level', {'name': 'Maximum level', 'value': 0})
    ])

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode(settings.WINDOW_SIZE, pygame.DOUBLEBUF)
        self.window_rect = self.window.get_rect()

        pygame.display.set_caption('Tetris')
        pygame.display.set_icon(helpers.load_image('icon.png'))

        self.current_tetrimino = None
        self.next_tetrimino = None
        self.started_playing_at = None

        self._load_fonts()
        self._load_sounds()

        stats_manager.load_stats(settings.STATS_FILE_NAME, self.stats)

        if os.path.isfile(settings.SAVE_FILE_NAME):
            save_game_manager.load_game(settings.SAVE_FILE_NAME, self, self.save_data)

            self.is_fast_falling = False

            self._load_random_music()

            self._toggle_pause(True)
        else:
            self._start_new_game()

    def _load_fonts(self):
        """Load the fonts."""
        logging.info('Loading fonts')

        self.fonts = {
            'normal': helpers.load_font('coolvetica.ttf', 18),
            'big': helpers.load_font('coolvetica.ttf', 30)
        }

    def _load_sounds(self):
        """Load the sound effects."""
        logging.info('Loading sounds')

        self.sounds = {
            'move': helpers.load_sound('move.ogg', volume=settings.SOUNDS_VOLUME),
            'rotate': helpers.load_sound('rotate.ogg', volume=settings.SOUNDS_VOLUME),
            'place': helpers.load_sound('place.ogg', volume=settings.SOUNDS_VOLUME),
            'lines_completed': helpers.load_sound('lines_completed.ogg', volume=settings.SOUNDS_VOLUME),
            'new_level': helpers.load_sound('new_level.ogg', volume=settings.SOUNDS_VOLUME)
        }

    def _load_random_music(self):
        """Load and play a random music."""
        logging.info('Loading random music')

        helpers.load_random_music(
            ['its_raining_pixels.wav', 'its_always_sunny_in_the_80s.wav'],
            volume=settings.MUSIC_VOLUME
        )

    def _start_new_game(self):
        """Start a new game."""
        logging.info('Initializing new game')

        self._update_play_time()

        self.fallen_blocks = []
        self.level = 1
        self.lines = 0
        self.score = 0
        self.duration = 0

        self.is_fast_falling = False

        self.started_playing_at = int(time.time())

        self._set_current_tetrimino()
        self._update_falling_interval()
        self._toggle_duration_counter(True)

        self._load_random_music()

        self.state = settings.GameState.PLAYING

    def _update_falling_interval(self, force=None):
        """Update the Tetrimino's falling event."""
        if force is not None:
            pygame.time.set_timer(settings.TETRIMINOS_FALLING_EVENT, force)
        else:
            value = settings.TETRIMINOS_INITIAL_FALLING_INTERVAL - self.level * settings.TETRIMINOS_FALLING_INTERVAL_DECREASE_STEP

            # Prevent the falling event timer to reach a value of zero or below,
            # thus preventing any blocks to fall.
            # Set an arbitrary - inhuman - value of 10 milliseconds instead so
            # the player can still - barely - play.
            # https://github.com/EpocDotFr/tetris/issues/1
            if value <= 0:
                value = 10

            pygame.time.set_timer(
                settings.TETRIMINOS_FALLING_EVENT,
                value
            )

    def _toggle_duration_counter(self, enable=True):
        """Update the game duration counter event."""
        pygame.time.set_timer(settings.GAME_DURATION_EVENT, 1000 if enable else 0) # Every seconds

    def _set_current_tetrimino(self):
        """Sets the current falling Tetrimino along the next Tetrimino."""
        if not self.next_tetrimino:
            self.current_tetrimino = self._get_random_tetrimino()(settings.PLAYGROUND_CENTERX, 0)
        else:
            self.current_tetrimino = self.next_tetrimino(settings.PLAYGROUND_CENTERX, 0)

        self.next_tetrimino = self._get_random_tetrimino()

        # Check if the game is over
        if self.current_tetrimino.will_collide(self.fallen_blocks):
            self._update_falling_interval(0)
            self._toggle_duration_counter(False)
            self.state = settings.GameState.GAME_OVER
            self._update_play_time()

            logging.info('Game over')

            self._update_game_stats()
            stats_manager.save_stats(settings.STATS_FILE_NAME, self.stats)

            if os.path.isfile(settings.SAVE_FILE_NAME):
                os.remove(settings.SAVE_FILE_NAME)

    def _get_random_tetrimino(self):
        """Get a random reference to a Tetrimino class."""
        return getattr(tetriminos, random.choice(tetriminos.__all__))

    def _toggle_pause(self, force=None, update_state=True):
        """Toggle pause on/off."""
        if force is False or (force is None and self.state in [settings.GameState.PAUSED, settings.GameState.SHOW_STATS]):
            self._update_falling_interval()
            self._toggle_duration_counter(True)

            self.started_playing_at = int(time.time())

            if update_state:
                self.state = settings.GameState.PLAYING

            logging.info('Game unpaused')
        elif force is True or (force is None and self.state not in [settings.GameState.PAUSED, settings.GameState.SHOW_STATS]):
            self._update_falling_interval(0)
            self._toggle_duration_counter(False)
            self._update_play_time()

            if update_state:
                self.state = settings.GameState.PAUSED

            logging.info('Game paused')

    def _toggle_stats(self, force=None):
        if force is False or (force is None and self.state == settings.GameState.SHOW_STATS):
            self._toggle_pause(False, False)

            self.state = settings.GameState.PLAYING

            logging.info('Hiding stats')
        elif force is True or (force is None and self.state != settings.GameState.SHOW_STATS):
            self._toggle_pause(True, False)

            self.state = settings.GameState.SHOW_STATS

            logging.info('Showing stats')

    def _update_play_time(self):
        """Update the play time in the stats."""
        if self.started_playing_at:
            self.stats['play_time']['value'] += int(time.time()) - self.started_playing_at

            self.started_playing_at = None

    def _update_game_stats(self):
        """Update the stats data after the game is over."""
        if self.score > self.stats['max_score']['value']:
            self.stats['max_score']['value'] = self.score

        if self.lines > self.stats['max_lines']['value']:
            self.stats['max_lines']['value'] = self.lines

        if self.level > self.stats['max_level']['value']:
            self.stats['max_level']['value'] = self.level

        if self.duration > self.stats['longest_game']['value']:
            self.stats['longest_game']['value'] = self.duration

        self.stats['overall_score']['value'] += self.score
        self.stats['overall_lines']['value'] += self.lines

        self.stats['games_played']['value'] += 1

        self._update_play_time()

    def _process_lines(self):
        """For each completed lines: remove them and make everything to fall."""
        completed_lines = {}

        # Count the number of blocks in each lines
        for block in self.fallen_blocks:
            if block.y not in completed_lines:
                completed_lines[block.y] = 0

            completed_lines[block.y] += 1

        # For each completed lines, remove each block in them
        for y, total in completed_lines.copy().items():
            if total == settings.COLS:
                # The list comprehension to prevent unexpected results when removing from self.fallen_blocks while looping on it
                for block in [block for block in self.fallen_blocks if block.y == y]:
                    self.fallen_blocks.remove(block)
            else:
                del completed_lines[y] # Remove uncompleted lines counts

        completed_lines_count = len(completed_lines)

        if completed_lines_count == 0: # There wasn't any completed lines at all
            return

        # Starting from the topmost line of the playground, make everything above an empty line to fall for one block down
        for y in range(0, settings.ROWS):
            if y not in completed_lines:
                continue

            for block in self.fallen_blocks:
                if block.y > y or block.is_bottommost():
                    continue

                block.y += 1

        # Compute and update the score
        score_to_add = completed_lines_count * settings.COMPLETED_LINE_SCORE

        # If four lines were completed at one time, it's a Tetris, so double the score
        if completed_lines_count == 4:
            score_to_add *= 2

        # If the playground is empty after the Tetrimino has fallen and lines has been removed: double the score (again)
        if not self.fallen_blocks:
            score_to_add *= 2

        self.score += score_to_add
        self.lines += completed_lines_count

        # Compute and update the new level (if applicable)
        new_level = len(list(range(0, self.lines, settings.LEVEL_INCREASE_LINES_STEP)))

        # Did we reached a new level of difficulty?
        if self.level != new_level:
            self.sounds['new_level'].play()

            self.level = new_level

            if not self.is_fast_falling: # If the player has pressed the down arrow, do not change the speed of the fall
                self._update_falling_interval()
        else:
            self.sounds['lines_completed'].play()

    def update(self):
        """Perform every updates of the game logic, events handling and drawing.
        Also known as the game loop."""

        # Events handling
        for event in pygame.event.get():
            event_handlers = [
                self._event_quit,
                self._event_falling_tetrimino,
                self._event_game_key,
                self._event_game_duration
            ]

            for handler in event_handlers:
                if handler(event):
                    break

        # Drawings
        self.window.fill(settings.WINDOW_BACKGROUND_COLOR)

        self._draw_playground()

        if self.state != settings.GameState.GAME_OVER:
            self._draw_blocks(self.current_tetrimino.blocks)

        self._draw_blocks(self.fallen_blocks)
        self._draw_info_panel()

        if self.state == settings.GameState.SHOW_STATS:
            self._draw_stats_screen()
        elif self.state == settings.GameState.PAUSED:
            self._draw_pause_screen()
        elif self.state == settings.GameState.GAME_OVER:
            self._draw_game_over_screen()

        # PyGame-related updates
        pygame.display.update()

        self.clock.tick(settings.FPS)

    # --------------------------------------------------------------------------
    # Events handlers

    def _event_quit(self, event):
        """Called when the game must be closed."""
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if self.state != settings.GameState.GAME_OVER:
                save_game_manager.save_game(settings.SAVE_FILE_NAME, self, self.save_data)

            self._update_play_time()
            stats_manager.save_stats(settings.STATS_FILE_NAME, self.stats)

            pygame.quit()
            sys.exit()

        return False

    def _event_falling_tetrimino(self, event):
        """Makes the current tetrimino to fall."""
        if event.type != settings.TETRIMINOS_FALLING_EVENT:
            return False

        if not self.current_tetrimino.make_it_fall(self.fallen_blocks):
            self.sounds['place'].play()

            self.fallen_blocks.extend(self.current_tetrimino.blocks.copy())

            self._process_lines()
            self._set_current_tetrimino()

        return True

    def _event_game_duration(self, event):
        """Count the duration of the current game."""
        if event.type != settings.GAME_DURATION_EVENT:
            return False

        self.duration += 1

        return True

    def _event_game_key(self, event):
        """Handle the game keys."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAUSE and self.state not in [settings.GameState.GAME_OVER, settings.GameState.SHOW_STATS]:
                self._toggle_pause()

                return True
            elif event.key == pygame.K_F1:
                self._start_new_game()

                return True
            elif event.key == pygame.K_F2:
                self._toggle_stats()

                return True
            elif event.key == pygame.K_LEFT and self.state not in [settings.GameState.PAUSED, settings.GameState.GAME_OVER]:
                if self.current_tetrimino.move_left(self.fallen_blocks):
                    self.sounds['move'].play()

                    return True
            elif event.key == pygame.K_RIGHT and self.state not in [settings.GameState.PAUSED, settings.GameState.GAME_OVER]:
                if self.current_tetrimino.move_right(self.fallen_blocks):
                    self.sounds['move'].play()

                    return True
            elif event.key == pygame.K_DOWN and self.state not in [settings.GameState.PAUSED, settings.GameState.GAME_OVER]:
                self._update_falling_interval(settings.TETRIMINOS_FAST_FALLING_INTERVAL)
                self.is_fast_falling = True

                return True
            elif event.key == pygame.K_UP and self.state not in [settings.GameState.PAUSED, settings.GameState.GAME_OVER]:
                if self.current_tetrimino.rotate(self.fallen_blocks):
                    self.sounds['rotate'].play()

                    return True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN and self.state not in [settings.GameState.PAUSED, settings.GameState.GAME_OVER]:
                self._update_falling_interval()
                self.is_fast_falling = False

                return True

        return False

    # --------------------------------------------------------------------------
    # Drawing handlers

    def _draw_playground(self):
        """Draw the playground."""
        # Background behind the playground
        pygame.draw.rect(
            self.window,
            settings.PLAYGROUND_BACKGROUND_COLOR,
            pygame.Rect(
                (0, 0),
                (settings.PLAYGROUND_WIDTH, settings.PLAYGROUND_HEIGHT)
            )
        )

        # The playground grid (if it should be rendered)
        if settings.DRAW_GRID:
            for x in range(0, settings.COLS + 1):
                pygame.draw.rect(
                    self.window,
                    settings.GRID_COLOR,
                    pygame.Rect(
                        (x * settings.BLOCKS_SIDE_SIZE + (x - 1) * settings.GRID_SPACING, 0),
                        (settings.GRID_SPACING, settings.PLAYGROUND_HEIGHT)
                    )
                )

            for y in range(0, settings.ROWS + 1):
                pygame.draw.rect(
                    self.window,
                    settings.GRID_COLOR,
                    pygame.Rect(
                        (0, y * settings.BLOCKS_SIDE_SIZE + (y - 1) * settings.GRID_SPACING),
                        (settings.PLAYGROUND_WIDTH, settings.GRID_SPACING)
                    )
                )

    def _draw_blocks(self, blocks):
        """Draw a collection of blocks on the playground."""
        for block in blocks:
            block.rect.top = block.y * settings.BLOCKS_SIDE_SIZE + block.y * settings.GRID_SPACING
            block.rect.left = block.x * settings.BLOCKS_SIDE_SIZE + block.x * settings.GRID_SPACING

            self.window.blit(block.image, block.rect)

    def _draw_next_tetrimino(self, x, y):
        """Draws the next Tetrimino in the info panel."""
        for pat_y, y_val in enumerate(self.next_tetrimino.pattern):
            for pat_x, x_val in enumerate(self.next_tetrimino.pattern[pat_y]):
                if self.next_tetrimino.pattern[pat_y][pat_x] == 1:
                    block = tetriminos.Block(self.next_tetrimino.background_color, pat_x, pat_y)

                    block.rect.top = block.y * settings.BLOCKS_SIDE_SIZE + block.y * settings.GRID_SPACING + y
                    block.rect.left = block.x * settings.BLOCKS_SIDE_SIZE + block.x * settings.GRID_SPACING + x

                    self.window.blit(block.image, block.rect)

    def _draw_info_panel(self):
        """Draws the information panel."""
        next_tetrimino_label = self.fonts['normal'].render('Next', True, settings.TEXT_COLOR)
        next_tetrimino_label_rect = next_tetrimino_label.get_rect()
        next_tetrimino_label_rect.left = settings.PLAYGROUND_WIDTH + 20
        next_tetrimino_label_rect.top = 15

        self.window.blit(next_tetrimino_label, next_tetrimino_label_rect)

        self._draw_next_tetrimino(settings.PLAYGROUND_WIDTH + 20, next_tetrimino_label_rect.bottom + 10)

        spacing = next_tetrimino_label_rect.bottom + 110

        for info in self.infos:
            # Label
            info_label = self.fonts['normal'].render(info['name'], True, settings.TEXT_COLOR)
            info_label_rect = info_label.get_rect()
            info_label_rect.left = settings.PLAYGROUND_WIDTH + 20
            info_label_rect.top = spacing

            self.window.blit(info_label, info_label_rect)

            # Value
            value = getattr(self, info['value'])
            value_format = info['format'] if 'format' in info else str

            info_value = self.fonts['normal'].render(value_format(value), True, settings.TEXT_COLOR)
            info_value_rect = info_value.get_rect()
            info_value_rect.right = self.window_rect.w - 20
            info_value_rect.top = spacing

            self.window.blit(info_value, info_value_rect)

            spacing += 35

    def _draw_fullscreen_transparent_background(self):
        """Draws a transparent rect that takes the whole window."""
        rect = pygame.Surface(self.window_rect.size)
        rect.set_alpha(230)
        rect.fill(settings.WINDOW_BACKGROUND_COLOR)

        self.window.blit(
            rect,
            pygame.Rect(
                (0, 0),
                self.window_rect.size
            )
        )

    def _draw_fullscreen_window(self, title, text):
        """Draws a title and a text in the middle of the screen."""
        if isinstance(text, str):
            text = [text]

        self._draw_fullscreen_transparent_background()

        # Title
        title_label = self.fonts['big'].render(title, True, settings.TEXT_COLOR)
        title_label_rect = title_label.get_rect()
        title_label_rect.center = self.window_rect.center
        title_label_rect.centery -= 15

        self.window.blit(title_label, title_label_rect)

        # Text
        spacing = 15

        for t in text:
            text_label = self.fonts['normal'].render(t, True, settings.TEXT_COLOR)
            text_label_rect = text_label.get_rect()
            text_label_rect.center = self.window_rect.center
            text_label_rect.centery += spacing

            self.window.blit(text_label, text_label_rect)

            spacing += 20

    def _draw_pause_screen(self):
        """Draws the Pause screen."""
        self._draw_fullscreen_window('Pause', 'Press "Pause" again to continue.')

    def _draw_game_over_screen(self):
        """Draws the Game over screen."""
        recap_string = [
            'You completed {} lines, which gained you'.format(self.lines),
            'to the level {} with a score of {}'.format(self.level, self.score),
            'in {}.'.format(helpers.humanize_seconds(self.duration)),
            'Press "F1" to start a new game.'
        ]

        self._draw_fullscreen_window('Game over!', recap_string)

    def _draw_stats_screen(self):
        """Draws the Stats screen."""
        self._draw_fullscreen_transparent_background()

        # Title
        title_label = self.fonts['big'].render('Statistics', True, settings.TEXT_COLOR)
        title_label_rect = title_label.get_rect()
        title_label_rect.centerx = self.window_rect.centerx
        title_label_rect.top = 20

        self.window.blit(title_label, title_label_rect)

        # The stats themselves
        spacing = title_label_rect.bottom + 30

        for key, stat in self.stats.items():
            # Stat label
            stat_label = self.fonts['normal'].render(stat['name'], True, settings.TEXT_COLOR)
            stat_label_rect = stat_label.get_rect()
            stat_label_rect.left = 40
            stat_label_rect.top = spacing

            self.window.blit(stat_label, stat_label_rect)

            # Stat value
            stat_value_format = stat['format'] if 'format' in stat else str

            stat_value = self.fonts['normal'].render(stat_value_format(stat['value']), True, settings.TEXT_COLOR)
            stat_value_rect = stat_value.get_rect()
            stat_value_rect.right = self.window_rect.w - 40
            stat_value_rect.top = spacing

            self.window.blit(stat_value, stat_value_rect)

            spacing += 35
