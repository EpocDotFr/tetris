import pygame
import tetriminos
import settings
import random
import utils
import sys


class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode((settings.COLS * settings.BLOCKS_SIDE_SIZE + (settings.COLS - 1) * settings.GRID_SPACING, settings.ROWS * settings.BLOCKS_SIDE_SIZE + (settings.ROWS - 1) * settings.GRID_SPACING), pygame.DOUBLEBUF)
        self.window_rect = self.window.get_rect()

        pygame.display.set_caption('Tetris')
        pygame.display.set_icon(utils.load_image('icon.png'))

        self._init_new_game()

    def _init_new_game(self):
        self.fallen_blocks = []
        self.current_tetrimino = None

        pygame.time.set_timer(settings.TETRIMINOS_FALLING_EVENT, settings.TETRIMINOS_FALLING_INTERVAL)

    def _set_current_tetrimino(self):
        if self.current_tetrimino:
            return

        self.current_tetrimino = getattr(tetriminos, random.choice(tetriminos.__all__))()

    def update(self):
        self._set_current_tetrimino()

        # ----------------------------------------------------------------------
        # Events handling

        for event in pygame.event.get():
            self._event_quit(event)
            self._event_falling_tetrimino(event)
            self._event_game_key(event)

        # ----------------------------------------------------------------------
        # Drawing

        self.window.fill((255, 255, 255))

        self._draw_grid()
        self._draw_blocks(self.current_tetrimino.blocks)
        self._draw_blocks(self.fallen_blocks)

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

        self.current_tetrimino.make_it_fall() # TODO Check it does not go out of the window

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

    def _draw_grid(self):
        if settings.DRAW_GRID:
            for x in range(1, settings.COLS):
                pos = pygame.Rect((x * settings.BLOCKS_SIDE_SIZE + (x - 1) * settings.GRID_SPACING, 0), (settings.GRID_SPACING, self.window_rect.h))

                pygame.draw.rect(self.window, settings.GRID_COLOR, pos)

            for y in range(1, settings.ROWS):
                pos = pygame.Rect((0, y * settings.BLOCKS_SIDE_SIZE + (y - 1) * settings.GRID_SPACING), (self.window_rect.w, settings.GRID_SPACING))

                pygame.draw.rect(self.window, settings.GRID_COLOR, pos)

    def _draw_blocks(self, blocks):
        for block in blocks:
            block.rect.top = block.pos_y * settings.BLOCKS_SIDE_SIZE + block.pos_y * settings.GRID_SPACING
            block.rect.left = block.pos_x * settings.BLOCKS_SIDE_SIZE + block.pos_x * settings.GRID_SPACING

            self.window.blit(block.image, block.rect)
