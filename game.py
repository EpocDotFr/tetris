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

        logging.info('Loading fonts')

        self.normal_font = utils.load_font('coolvetica.ttf', 18)

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

        self.current_tetrimino = getattr(tetriminos, random.choice(tetriminos.__all__))(x, 0)

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

        if event.key == pygame.K_LEFT:
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
        pos = pygame.Rect(
            (0, 0),
            (settings.PLAYGROUND_WIDTH, settings.PLAYGROUND_HEIGHT)
        )

        pygame.draw.rect(self.window, settings.PLAYGROUND_BACKGROUND_COLOR, pos)

        # The playground grid (if it should be rendered)
        if settings.DRAW_GRID:
            for x in range(1, settings.COLS):
                pos = pygame.Rect(
                    (x * settings.BLOCKS_SIDE_SIZE + (x - 1) * settings.GRID_SPACING, 0),
                    (settings.GRID_SPACING, settings.PLAYGROUND_HEIGHT)
                )

                pygame.draw.rect(self.window, settings.GRID_COLOR, pos)

            for y in range(1, settings.ROWS):
                pos = pygame.Rect(
                    (0, y * settings.BLOCKS_SIDE_SIZE + (y - 1) * settings.GRID_SPACING),
                    (settings.PLAYGROUND_WIDTH, settings.GRID_SPACING)
                )

                pygame.draw.rect(self.window, settings.GRID_COLOR, pos)

    def _draw_blocks(self, blocks):
        for block in blocks:
            block.rect.top = block.y * settings.BLOCKS_SIDE_SIZE + block.y * settings.GRID_SPACING
            block.rect.left = block.x * settings.BLOCKS_SIDE_SIZE + block.x * settings.GRID_SPACING

            self.window.blit(block.image, block.rect)

    def _draw_info_panel(self):
        # Next Tetrimino
        next_tetrimino_label = self.normal_font.render('Next', True, settings.TEXT_COLOR)
        next_tetrimino_label_rect = next_tetrimino_label.get_rect()
        next_tetrimino_label_rect.left = settings.PLAYGROUND_WIDTH + 20
        next_tetrimino_label_rect.top = 35

        self.window.blit(next_tetrimino_label, next_tetrimino_label_rect)

        # Level label
        level_label = self.normal_font.render('Level', True, settings.TEXT_COLOR)
        level_label_rect = level_label.get_rect()
        level_label_rect.left = settings.PLAYGROUND_WIDTH + 20
        level_label_rect.top = 100

        self.window.blit(level_label, level_label_rect)

        # Level value
        level_value = self.normal_font.render('Level', True, settings.TEXT_COLOR)
        level_value_rect = level_value.get_rect()
        level_value_rect.left = settings.PLAYGROUND_WIDTH + 20
        level_value_rect.top = 100

        self.window.blit(level_value, level_value_rect)

        # Lines label
        lines_label = self.normal_font.render('Lines', True, settings.TEXT_COLOR)
        lines_label_rect = lines_label.get_rect()
        lines_label_rect.left = settings.PLAYGROUND_WIDTH + 20
        lines_label_rect.top = 130

        self.window.blit(lines_label, lines_label_rect)

        # Score label
        score_label = self.normal_font.render('Score', True, settings.TEXT_COLOR)
        score_label_rect = score_label.get_rect()
        score_label_rect.left = settings.PLAYGROUND_WIDTH + 20
        score_label_rect.top = 160

        self.window.blit(score_label, score_label_rect)
