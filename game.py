import tetriminos
import settings
import logging
import helpers
import random
import pygame
import pickle
import json
import time
import math
import sys
import os


class Game:
    save_data = [
        'fallen_blocks',
        'level',
        'lines',
        'score',
        'current_tetrimino',
        'next_tetrimino'
    ]

    infos = [
        {'name': 'Level', 'value': 'level'},
        {'name': 'Lines', 'value': 'lines'},
        {'name': 'Score', 'value': 'score'}
    ]

    stats = {
        'play_time': {'name': 'Play time', 'value': 0},
        'overall_score': {'name': 'Overall score', 'value': 0},
        'overall_lines': {'name': 'Overall lines', 'value': 0},
        'max_score': {'name': 'Maximum reached score', 'value': 0},
        'max_lines': {'name': 'Maximum reached lines', 'value': 0},
        'max_level': {'name': 'Maximum reached level', 'value': 0},
        'games_played': {'name': 'Total games played', 'value': 0}
    }

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode(settings.WINDOW_SIZE, pygame.DOUBLEBUF)
        self.window_rect = self.window.get_rect()

        pygame.display.set_caption('Tetris')
        pygame.display.set_icon(helpers.load_image('icon.png'))

        self.current_tetrimino = None
        self.next_tetrimino = None

        logging.info('Loading fonts')

        self.normal_font = helpers.load_font('coolvetica.ttf', 18)
        self.big_font = helpers.load_font('coolvetica.ttf', 30)

        self._load_stats()
        self._start_new_game()

    def _start_new_game(self):
        """Start a new game."""
        logging.info('Initializing new game')

        self.fallen_blocks = []
        self.level = 1
        self.lines = 0
        self.score = 0

        self.is_paused = False
        self.is_game_over = False
        self.show_stats = False

        self._set_current_tetrimino()
        self._enable_or_update_falling_interval()

    def _enable_or_update_falling_interval(self):
        """Starts othe Tetrimino's falling."""
        pygame.time.set_timer(settings.TETRIMINOS_FALLING_EVENT, settings.TETRIMINOS_INITIAL_FALLING_INTERVAL - self.level * settings.FALLING_INTERVAL_DECREASE_STEP)

        self.started_playing_at = int(time.time())

    def _disable_falling_interval(self):
        """Stops the Tetrimino's falling."""
        pygame.time.set_timer(settings.TETRIMINOS_FALLING_EVENT, 0)

        self._update_play_time()

    def _set_current_tetrimino(self):
        """Sets the current falling Tetrimino along the next Tetrimino."""
        x = math.floor((settings.COLS - 1) / 2)

        if not self.next_tetrimino:
            self.current_tetrimino = self._get_random_tetrimino()(x, 0)
        else:
            self.current_tetrimino = self.next_tetrimino(x, 0)

        self.next_tetrimino = self._get_random_tetrimino()

        # Check if the game is over
        if self.current_tetrimino.will_collide(self.fallen_blocks):
            self._disable_falling_interval()
            self.is_game_over = True

            logging.info('Game over')

            self._update_game_stats()
            self._save_stats()

    def _get_random_tetrimino(self):
        """Get a random reference to a Tetrimino class."""
        return getattr(tetriminos, random.choice(tetriminos.__all__))

    def _toggle_pause(self, force=None):
        """Toggle pause on/off."""
        if self.is_game_over or self.show_stats:
            return

        if self.is_paused or force is False:
            self._enable_or_update_falling_interval()
            self.is_paused = False

            logging.info('Game unpaused')
        elif not self.is_paused or force is True:
            self._disable_falling_interval()
            self.is_paused = True

            logging.info('Game paused')

    def _toggle_stats(self, force=None):
        if self.show_stats or force is False:
            self.show_stats = False

            self._toggle_pause(False)

            logging.info('Hiding stats')
        elif not self.show_stats or force is True:
            self.show_stats = True

            self._toggle_pause(True)

            logging.info('Showing stats')

    def _load_game(self):
        """Load a saved game."""
        if not os.path.isfile(settings.SAVE_FILE_NAME):
            logging.info('Save file does not exists')
            return

        logging.info('Loading saved game')

        with open(settings.SAVE_FILE_NAME, 'rb') as f:
            data = pickle.load(f)

        for sd in self.save_data:
            if sd in data:
                setattr(self, sd, data[sd])

        self.is_paused = False
        self.is_game_over = False
        self.show_stats = False

        self._toggle_pause(True)

    def _save_game(self):
        """Save the current game."""
        if self.is_game_over:
            return

        logging.info('Saving current game')

        data = {}

        for sd in self.save_data:
            data[sd] = getattr(self, sd)

        with open(settings.SAVE_FILE_NAME, 'wb') as f:
            pickle.dump(data, f)

    def _load_stats(self):
        """Save the current stats to a JSON file."""
        if not os.path.isfile(settings.STATS_FILE_NAME):
            logging.info('Stats file does not exists')
            return

        logging.info('Loading stats')

        with open(settings.STATS_FILE_NAME, 'r', encoding='utf-8') as f:
            data = json.load(f)

            for key, value in data.items():
                self.stats[key]['value'] = value

    def _save_stats(self):
        """Load stats from a JSON file."""
        logging.info('Saving stats')

        data = {}

        for key, stat in self.stats.items():
            data[key] = stat['value']

        with open(settings.STATS_FILE_NAME, 'w', encoding='utf-8') as f:
            json.dump(data, f)

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
                for block in self.fallen_blocks: # TODO For an unknown reason, not all blocks are being removed
                    if block.y != y:
                        continue

                    self.fallen_blocks.remove(block)
            else:
                del completed_lines[y] # Remove uncompleted lines counts

        completed_lines_count = len(completed_lines)

        if completed_lines_count == 0: # There wasn't any completed lines at all
            return

        # Make all blocks above the bottommost completed line to fall
        # TODO
        # for i in range(0, completed_lines_count):
        #     for block in self.fallen_blocks:
        #         if block.is_bottommost():
        #             continue

        #         block.y += 1

        # Compute and update the score as well as the lines count
        score_to_add = completed_lines_count * settings.COMPLETED_LINE_SCORE

        # If four lines were completed at one time, it's a Tetris, so double the score
        if completed_lines_count == 4:
            score_to_add *= 2

        self.score += score_to_add
        self.lines += completed_lines_count

        new_level = len(list(range(0, self.lines, settings.LEVEL_INCREASE_STEP)))

        # Did we reached a new level of difficulty?
        if self.level != new_level:
            self.level = new_level

            self._enable_or_update_falling_interval()

    def update(self):
        """Perform every updates of the game logic, events handling and drawing.
        Also known as the game loop."""

        # Events handling
        for event in pygame.event.get():
            self._event_quit(event)
            self._event_falling_tetrimino(event)
            self._event_game_key(event)

        # Drawings
        self.window.fill(settings.WINDOW_BACKGROUND_COLOR)

        self._draw_playground()

        if not self.is_game_over:
            self._draw_blocks(self.current_tetrimino.blocks)

        self._draw_blocks(self.fallen_blocks)
        self._draw_info_panel()
        self._draw_stats_screen()
        self._draw_pause_screen()
        self._draw_game_over_screen()

        # PyGame-related updates
        pygame.display.update()

        self.clock.tick(settings.FPS)

    # --------------------------------------------------------------------------
    # Events handlers

    def _event_quit(self, event):
        """Called when the game must be closed."""
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._save_game()
            self._update_play_time()
            self._save_stats()
            pygame.quit()
            sys.exit()

    def _event_falling_tetrimino(self, event):
        """Makes the current tetrimino to fall."""
        if event.type != settings.TETRIMINOS_FALLING_EVENT:
            return

        if not self.current_tetrimino.make_it_fall(self.fallen_blocks):
            self.fallen_blocks.extend(self.current_tetrimino.blocks.copy())

            self._process_lines()
            self._set_current_tetrimino()

    def _event_game_key(self, event):
        """Handle the game keys."""
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_PAUSE:
            self._toggle_pause()
        elif event.key == pygame.K_F1:
            self._start_new_game()
        elif event.key == pygame.K_F2:
            self._load_game()
        elif event.key == pygame.K_F3:
            self._toggle_stats()
        elif event.key == pygame.K_LEFT:
            self.current_tetrimino.move_left(self.fallen_blocks)
        elif event.key == pygame.K_RIGHT:
            self.current_tetrimino.move_right(self.fallen_blocks)
        elif event.key == pygame.K_DOWN:
            pass # TODO Make the Tetrimino to fall faster
        elif event.key == pygame.K_UP:
            self.current_tetrimino.rotate()

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
        next_tetrimino_label = self.normal_font.render('Next', True, settings.TEXT_COLOR)
        next_tetrimino_label_rect = next_tetrimino_label.get_rect()
        next_tetrimino_label_rect.left = settings.PLAYGROUND_WIDTH + 20
        next_tetrimino_label_rect.top = 15

        self.window.blit(next_tetrimino_label, next_tetrimino_label_rect)

        self._draw_next_tetrimino(settings.PLAYGROUND_WIDTH + 20, next_tetrimino_label_rect.bottom + 10)

        spacing = next_tetrimino_label_rect.bottom + 110

        for info in self.infos:
            # Label
            info_label = self.normal_font.render(info['name'], True, settings.TEXT_COLOR)
            info_label_rect = info_label.get_rect()
            info_label_rect.left = settings.PLAYGROUND_WIDTH + 20
            info_label_rect.top = spacing

            self.window.blit(info_label, info_label_rect)

            # Value
            value = getattr(self, info['value'])
            value_format = info['format'] if 'format' in info else str

            info_value = self.normal_font.render(value_format(value), True, settings.TEXT_COLOR)
            info_value_rect = info_value.get_rect()
            info_value_rect.right = self.window_rect.w - 20
            info_value_rect.top = spacing

            self.window.blit(info_value, info_value_rect)

            spacing += 35

    def _draw_fullscreen_transparent_background(self):
        """Draws a transparent rect that takes the whole window."""
        rect = pygame.Surface(self.window_rect.size)
        rect.set_alpha(200)
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
        title_label = self.big_font.render(title, True, settings.TEXT_COLOR)
        title_label_rect = title_label.get_rect()
        title_label_rect.center = self.window_rect.center
        title_label_rect.centery -= 15

        self.window.blit(title_label, title_label_rect)

        # Text
        spacing = 15

        for t in text:
            text_label = self.normal_font.render(t, True, settings.TEXT_COLOR)
            text_label_rect = text_label.get_rect()
            text_label_rect.center = self.window_rect.center
            text_label_rect.centery += spacing

            self.window.blit(text_label, text_label_rect)

            spacing += 20

    def _draw_pause_screen(self):
        """Draws the Pause screen."""
        if self.is_paused and not self.show_stats:
            self._draw_fullscreen_window('Pause', 'Press "Pause" again to continue.')

    def _draw_game_over_screen(self):
        """Draws the Game over screen."""
        if self.is_game_over and not self.show_stats:
            recap_string = [
                'You completed {} lines, which gained you'.format(self.lines),
                'to the level {} with a score of {}.'.format(self.level, self.score),
                'Press "F1" to start a new game.'
            ]

            self._draw_fullscreen_window('Game over!', recap_string)

    def _draw_stats_screen(self):
        """Draws the Stats screen."""
        if self.show_stats:
            self._draw_fullscreen_transparent_background()

            # Title
            title_label = self.big_font.render('Statistics', True, settings.TEXT_COLOR)
            title_label_rect = title_label.get_rect()
            title_label_rect.centerx = self.window_rect.centerx
            title_label_rect.top = 20

            self.window.blit(title_label, title_label_rect)

            # The stats themselves
            spacing = title_label_rect.bottom + 30

            for key, stat in self.stats.items():
                # Stat label
                stat_label = self.normal_font.render(stat['name'], True, settings.TEXT_COLOR)
                stat_label_rect = stat_label.get_rect()
                stat_label_rect.left = 40
                stat_label_rect.top = spacing

                self.window.blit(stat_label, stat_label_rect)

                # Stat value
                stat_value_format = stat['format'] if 'format' in stat else str

                stat_value = self.normal_font.render(stat_value_format(stat['value']), True, settings.TEXT_COLOR)
                stat_value_rect = stat_value.get_rect()
                stat_value_rect.right = self.window_rect.w - 40
                stat_value_rect.top = spacing

                self.window.blit(stat_value, stat_value_rect)

                spacing += 35
