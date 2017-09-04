import pygame
import random
import sys
import os


VERSION = '0.1'
FPS = 30
BLOCKS_SIDE_SIZE = 20
COLS = 12
ROWS = 30
TETRIMINOS_FALLING_EVENT = pygame.USEREVENT + 1
TETRIMINOS_FALLING_INTERVAL = 1000
DRAW_GRID = True


class Block(pygame.sprite.Sprite):
    tetrimino = None

    def __init__(self, tetrimino):
        super(Block, self).__init__()

        self.tetrimino = tetrimino

        self._draw()

    def _draw(self):
        self.image = pygame.Surface((BLOCKS_SIDE_SIZE, BLOCKS_SIDE_SIZE), pygame.SRCALPHA, 32).convert_alpha()
        self.rect = self.image.get_rect()

        self.image.fill(self.tetrimino.background_color)


class Tetrimino(pygame.sprite.Group):
    background_color = None
    pattern = None
    rows = None
    cols = None

    def __init__(self):
        super(Tetrimino, self).__init__()

        self._draw()

    def _draw(self):
        self.rows = len(self.pattern)
        self.cols = len(self.pattern[0])

        self.image = pygame.Surface((self.cols * BLOCKS_SIDE_SIZE, self.rows * BLOCKS_SIDE_SIZE), pygame.SRCALPHA, 32).convert_alpha()
        self.rect = self.image.get_rect()

        for x, x_val in enumerate(self.pattern):
            for y, y_val in enumerate(self.pattern[x]):
                if self.pattern[x][y] == 1:
                    block = Block(tetrimino=self)

                    block.rect.topleft = (y * BLOCKS_SIDE_SIZE, x * BLOCKS_SIDE_SIZE)

                    self.image.blit(block.image, block.rect)

                    self.add(block)

    def rotate(self):
        prev_post = self.rect.topleft

        self.pattern = list(zip(*self.pattern[::-1]))
        self.image = pygame.transform.rotate(self.image, -90)
        self.rect = self.image.get_rect()
        self.rect.topleft = prev_post

    def __repr__(self):
        return '<{}> {}'.format(self.__class__.__name__, self.pattern)


class ITetrimino(Tetrimino):
    background_color = (0, 255, 255)
    pattern = [
        [1],
        [1],
        [1],
        [1]
    ]


class JTetrimino(Tetrimino):
    background_color = (0, 0, 255)
    pattern = [
        [0, 1],
        [0, 1],
        [0, 1],
        [1, 1]
    ]


class LTetrimino(Tetrimino):
    background_color = (255, 165, 0)
    pattern = [
        [1, 0],
        [1, 0],
        [1, 0],
        [1, 1]
    ]


class OTetrimino(Tetrimino):
    background_color = (255, 255, 0)
    pattern = [
        [1, 1],
        [1, 1]
    ]


class STetrimino(Tetrimino):
    background_color = (128, 255, 0)
    pattern = [
        [1, 0],
        [1, 1],
        [0, 1]
    ]


class TTetrimino(Tetrimino):
    background_color = (128, 0, 128)
    pattern = [
        [1, 1, 1],
        [0, 1, 0]
    ]


class ZTetrimino(Tetrimino):
    background_color = (255, 0, 0)
    pattern = [
        [0, 1],
        [1, 1],
        [1, 0]
    ]


def run():
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    pygame.init()

    clock = pygame.time.Clock()

    window = pygame.display.set_mode((COLS * BLOCKS_SIDE_SIZE, ROWS * BLOCKS_SIDE_SIZE), pygame.DOUBLEBUF)

    pygame.display.set_caption('Tetris')

    window_rect = window.get_rect()

    well = {}

    for x in range(0, COLS):
        well[x] = {}

        for y in range(0, ROWS):
            well[x][y] = None

    current_tetrimino = None
    pygame.time.set_timer(TETRIMINOS_FALLING_EVENT, TETRIMINOS_FALLING_INTERVAL)

    while True:
        if not current_tetrimino:
            current_tetrimino = random.choice([
                ITetrimino,
                JTetrimino,
                LTetrimino,
                OTetrimino,
                STetrimino,
                TTetrimino,
                ZTetrimino
            ])()

            current_tetrimino.rect.left = (COLS // 2) * ((current_tetrimino.cols // 2) * BLOCKS_SIDE_SIZE)
            current_tetrimino.rect.top = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == TETRIMINOS_FALLING_EVENT:
                if current_tetrimino.rect.bottom + BLOCKS_SIDE_SIZE > window_rect.h:
                    current_tetrimino = None
                else:
                    current_tetrimino.rect.bottom += BLOCKS_SIDE_SIZE
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_LEFT and current_tetrimino.rect.left - BLOCKS_SIDE_SIZE >= 0:
                    current_tetrimino.rect.left -= BLOCKS_SIDE_SIZE
                elif event.key == pygame.K_RIGHT and current_tetrimino.rect.right + BLOCKS_SIDE_SIZE <= window_rect.w:
                    current_tetrimino.rect.left += BLOCKS_SIDE_SIZE
                elif event.key == pygame.K_DOWN:
                    pass
                elif event.key == pygame.K_UP:
                    current_tetrimino.rotate()

        window.fill((255, 255, 255))

        current_tetrimino.draw(window)

        if DRAW_GRID:
            for x in range(0, COLS):
                pygame.draw.line(window, (225, 225, 225), (x * BLOCKS_SIDE_SIZE, 0), (x * BLOCKS_SIDE_SIZE, window_rect.h))

                for y in range(0, ROWS):
                    pygame.draw.line(window, (225, 225, 225), (0, y * BLOCKS_SIDE_SIZE), (window_rect.w, y * BLOCKS_SIDE_SIZE))

        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    run()
