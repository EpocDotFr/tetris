import pygame
import tetriminos
import logging
import settings
import random
import utils
import math
import sys


class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode(settings.WINDOW_SIZE, pygame.DOUBLEBUF)
        self.window_rect = self.window.get_rect()

        pygame.display.set_caption('Tetris')
        pygame.display.set_icon(utils.load_image('icon.png'))

        self.current_tetrimino = None
        self.next_tetrimino = None
        self.is_paused = False

        logging.info('Loading fonts')

        self.normal_font = utils.load_font('coolvetica.ttf', 18)
        self.big_font = utils.load_font('coolvetica.ttf', 30)

        self._new_game()

    def _new_game(self):
        self.fallen_blocks = []
        self.level = 1
        self.lines = 0
        self.score = 0

        self._set_current_tetrimino()

        pygame.time.set_timer(settings.TETRIMINOS_FALLING_EVENT, settings.TETRIMINOS_FALLING_INTERVAL)

    def _set_current_tetrimino(self):
        x = math.floor((settings.COLS - 1) / 2)

        if not self.next_tetrimino:
            self.current_tetrimino = self._get_random_tetrimino()(x, 0)
        else:
            self.current_tetrimino = self.next_tetrimino(x, 0)

        self.next_tetrimino = self._get_random_tetrimino()

    def _get_random_tetrimino(self):
        return getattr(tetriminos, random.choice(tetriminos.__all__))

    def _toggle_pause(self):
        if self.is_paused:
            pygame.time.set_timer(settings.TETRIMINOS_FALLING_EVENT, settings.TETRIMINOS_FALLING_INTERVAL)
            self.is_paused = False
        else:
            pygame.time.set_timer(settings.TETRIMINOS_FALLING_EVENT, 0)
            self.is_paused = True

    def update(self):
        # ----------------------------------------------------------------------
        # Events handling

        for event in pygame.event.get():
            self._event_quit(event)
            self._event_falling_tetrimino(event)
            self._event_game_key(event)

        # ----------------------------------------------------------------------
        # Drawing

        self.window.fill(settings.WINDOW_BACKGROUND_COLOR)

        self._draw_playground()
        self._draw_blocks(self.current_tetrimino.blocks)
        self._draw_blocks(self.fallen_blocks)
        self._draw_info_panel()
        self._draw_pause()

        pygame.display.update()

        self.clock.tick(settings.FPS)

    # --------------------------------------------------------------------------
    # Events handlers

    def _event_quit(self, event):
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

    def _event_falling_tetrimino(self, event):
        if event.type != settings.TETRIMINOS_FALLING_EVENT:
            return

        if not self.current_tetrimino.make_it_fall():
            self.fallen_blocks.extend(self.current_tetrimino.blocks.copy())

            self._set_current_tetrimino()

    def _event_game_key(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_PAUSE:
            self._toggle_pause()
        elif event.key == pygame.K_LEFT:
            self.current_tetrimino.move_left() # TODO Check it does not go out of the window
        elif event.key == pygame.K_RIGHT:
            self.current_tetrimino.move_right() # TODO Check it does not go out of the window
        elif event.key == pygame.K_DOWN:
            self.current_tetrimino.drop() # TODO Check it does not go out of the window
        elif event.key == pygame.K_UP:
            self.current_tetrimino.rotate() # TODO Check it does not go out of the window

    # --------------------------------------------------------------------------
    # Drawing handlers

    def _draw_playground(self):
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
        for block in blocks:
            block.rect.top = block.y * settings.BLOCKS_SIDE_SIZE + block.y * settings.GRID_SPACING
            block.rect.left = block.x * settings.BLOCKS_SIDE_SIZE + block.x * settings.GRID_SPACING

            self.window.blit(block.image, block.rect)

    def _draw_next_tetrimino(self, x, y):
        for pat_y, y_val in enumerate(self.next_tetrimino.pattern):
            for pat_x, x_val in enumerate(self.next_tetrimino.pattern[pat_y]):
                if self.next_tetrimino.pattern[pat_y][pat_x] == 1:
                    block = tetriminos.Block(self.next_tetrimino.background_color, pat_x, pat_y)

                    block.rect.top = block.y * settings.BLOCKS_SIDE_SIZE + block.y * settings.GRID_SPACING + y
                    block.rect.left = block.x * settings.BLOCKS_SIDE_SIZE + block.x * settings.GRID_SPACING + x

                    self.window.blit(block.image, block.rect)

    def _draw_info_panel(self):
        # Next Tetrimino
        next_tetrimino_label = self.normal_font.render('Next', True, settings.TEXT_COLOR)
        next_tetrimino_label_rect = next_tetrimino_label.get_rect()
        next_tetrimino_label_rect.left = settings.PLAYGROUND_WIDTH + 20
        next_tetrimino_label_rect.top = 15

        self.window.blit(next_tetrimino_label, next_tetrimino_label_rect)

        self._draw_next_tetrimino(settings.PLAYGROUND_WIDTH + 20, next_tetrimino_label_rect.bottom + 10)

        # Level label
        level_label = self.normal_font.render('Level', True, settings.TEXT_COLOR)
        level_label_rect = level_label.get_rect()
        level_label_rect.left = settings.PLAYGROUND_WIDTH + 20
        level_label_rect.top = next_tetrimino_label_rect.bottom + 110

        self.window.blit(level_label, level_label_rect)

        # Level value
        level_value = self.normal_font.render(str(self.level), True, settings.TEXT_COLOR)
        level_value_rect = level_value.get_rect()
        level_value_rect.right = self.window_rect.w - 20
        level_value_rect.top = next_tetrimino_label_rect.bottom + 110

        self.window.blit(level_value, level_value_rect)

        # Lines label
        lines_label = self.normal_font.render('Lines', True, settings.TEXT_COLOR)
        lines_label_rect = lines_label.get_rect()
        lines_label_rect.left = settings.PLAYGROUND_WIDTH + 20
        lines_label_rect.top = level_label_rect.bottom + 15

        self.window.blit(lines_label, lines_label_rect)

        # Lines value
        lines_value = self.normal_font.render(str(self.lines), True, settings.TEXT_COLOR)
        lines_value_rect = lines_value.get_rect()
        lines_value_rect.right = self.window_rect.w - 20
        lines_value_rect.top = level_label_rect.bottom + 15

        self.window.blit(lines_value, lines_value_rect)

        # Score label
        score_label = self.normal_font.render('Score', True, settings.TEXT_COLOR)
        score_label_rect = score_label.get_rect()
        score_label_rect.left = settings.PLAYGROUND_WIDTH + 20
        score_label_rect.top = lines_value_rect.bottom + 15

        self.window.blit(score_label, score_label_rect)

        # Score value
        score_value = self.normal_font.render(str(self.score), True, settings.TEXT_COLOR)
        score_value_rect = score_value.get_rect()
        score_value_rect.right = self.window_rect.w - 20
        score_value_rect.top = lines_value_rect.bottom + 15

        self.window.blit(score_value, score_value_rect)

    def _draw_pause(self):
        if self.is_paused:
            # Transparent rect that takes the whole window
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

            # "Pause" text
            pause = self.big_font.render('Pause', True, settings.TEXT_COLOR)
            pause_rect = pause.get_rect()
            pause_rect.center = self.window_rect.center
            pause_rect.centery -= 15

            self.window.blit(pause, pause_rect)

            # Pause tutorial text
            pause_tutorial = self.normal_font.render('Press "Pause" again to continue', True, settings.TEXT_COLOR)
            pause_tutorial_rect = pause_tutorial.get_rect()
            pause_tutorial_rect.center = self.window_rect.center
            pause_tutorial_rect.centery += 15

            self.window.blit(pause_tutorial, pause_tutorial_rect)
