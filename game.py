import pygame
import tetriminos
import settings
import random
import utils
import sys


class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode((settings.COLS * settings.BLOCKS_SIDE_SIZE, settings.ROWS * settings.BLOCKS_SIDE_SIZE), pygame.DOUBLEBUF)
        self.window_rect = self.window.get_rect()

        pygame.display.set_caption('Tetris')
        pygame.display.set_icon(utils.load_image('icon.png'))

        self._init_new_game()

    def _init_new_game(self):
        self.well = {}

        for x in range(0, settings.COLS):
            self.well[x] = {}

            for y in range(0, settings.ROWS):
                self.well[x][y] = None

        self.current_tetrimino = None

        pygame.time.set_timer(settings.TETRIMINOS_FALLING_EVENT, settings.TETRIMINOS_FALLING_INTERVAL)

    def _set_current_tetrimino(self):
        if self.current_tetrimino:
            return

        self.current_tetrimino = getattr(tetriminos, random.choice(tetriminos.__all__))()

        self.current_tetrimino.rect.left = (settings.COLS // 2) * ((self.current_tetrimino.cols // 2) * settings.BLOCKS_SIDE_SIZE)
        self.current_tetrimino.rect.top = 0

    def update(self):
        self._set_current_tetrimino()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._event_quit()
            elif event.type == settings.TETRIMINOS_FALLING_EVENT:
                self._event_falling_tetrimino()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._event_quit()
                else:
                    self._event_game_key(event)

        self._draw()

        pygame.display.update()

        self.clock.tick(settings.FPS)

    # --------------------------------------------------------------------------
    # Events handlers

    def _event_quit(self):
        pygame.quit()
        sys.exit()

    def _event_falling_tetrimino(self):
        if self.current_tetrimino.rect.bottom + settings.BLOCKS_SIDE_SIZE > self.window_rect.h:
            self.current_tetrimino = None
        else:
            self.current_tetrimino.rect.bottom += settings.BLOCKS_SIDE_SIZE

    def _event_game_key(self, event):
        if event.key == pygame.K_LEFT and self.current_tetrimino.rect.left - settings.BLOCKS_SIDE_SIZE >= 0:
            self.current_tetrimino.rect.left -= settings.BLOCKS_SIDE_SIZE
        elif event.key == pygame.K_RIGHT and self.current_tetrimino.rect.right + settings.BLOCKS_SIDE_SIZE <= self.window_rect.w:
            self.current_tetrimino.rect.left += settings.BLOCKS_SIDE_SIZE
        elif event.key == pygame.K_DOWN:
            pass
        elif event.key == pygame.K_UP:
            self.current_tetrimino.rotate()

    # --------------------------------------------------------------------------
    # Drawing handlers

    def _draw(self):
        self.window.fill((255, 255, 255))

        self.current_tetrimino.draw(self.window)

        if settings.DRAW_GRID:
            for x in range(0, settings.COLS):
                pygame.draw.line(self.window, (225, 225, 225), (x * settings.BLOCKS_SIDE_SIZE, 0), (x * settings.BLOCKS_SIDE_SIZE, self.window_rect.h))

                for y in range(0, settings.ROWS):
                    pygame.draw.line(self.window, (225, 225, 225), (0, y * settings.BLOCKS_SIDE_SIZE), (self.window_rect.w, y * settings.BLOCKS_SIDE_SIZE))
