import pygame
import settings


class Block(pygame.sprite.Sprite):
    tetrimino = None

    def __init__(self, tetrimino):
        super(Block, self).__init__()

        self.tetrimino = tetrimino

        self._draw()

    def _draw(self):
        self.image = pygame.Surface((settings.BLOCKS_SIDE_SIZE, settings.BLOCKS_SIDE_SIZE), pygame.SRCALPHA, 32).convert_alpha()
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

        self.image = pygame.Surface((self.cols * settings.BLOCKS_SIDE_SIZE, self.rows * settings.BLOCKS_SIDE_SIZE), pygame.SRCALPHA, 32).convert_alpha()
        self.rect = self.image.get_rect()

        for x, x_val in enumerate(self.pattern):
            for y, y_val in enumerate(self.pattern[x]):
                if self.pattern[x][y] == 1:
                    block = Block(tetrimino=self)

                    block.rect.topleft = (y * settings.BLOCKS_SIDE_SIZE, x * settings.BLOCKS_SIDE_SIZE)

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
