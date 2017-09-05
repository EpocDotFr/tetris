import pygame
import settings


__all__ = [
    'ITetrimino',
    'JTetrimino',
    'LTetrimino',
    'OTetrimino',
    'STetrimino',
    'TTetrimino',
    'ZTetrimino'
]


class Block(pygame.sprite.Sprite):
    def __init__(self, background_color, x, y):
        super(Block, self).__init__()

        self.background_color = background_color
        self.x = x
        self.y = y

        self.image = pygame.Surface((settings.BLOCKS_SIDE_SIZE, settings.BLOCKS_SIDE_SIZE), pygame.SRCALPHA, 32).convert_alpha()
        self.image.fill(self.background_color)

        self.rect = self.image.get_rect()


class Tetrimino(pygame.sprite.Group):
    def __init__(self):
        super(Tetrimino, self).__init__()

        self._draw()

    def _draw(self):
        self._rows = len(self.pattern)
        self._cols = len(self.pattern[0])

        self.image = pygame.Surface((self._cols * settings.BLOCKS_SIDE_SIZE + (self._cols * settings.GRID_SPACING), self._rows * settings.BLOCKS_SIDE_SIZE + (self._rows * settings.GRID_SPACING)), pygame.SRCALPHA, 32).convert_alpha()
        self.rect = self.image.get_rect()

        for x, x_val in enumerate(self.pattern):
            for y, y_val in enumerate(self.pattern[x]):
                if self.pattern[x][y] == 1:
                    block = Block()

                    block.rect.topleft = (y * settings.BLOCKS_SIDE_SIZE + ((y + 1) * settings.GRID_SPACING), x * settings.BLOCKS_SIDE_SIZE + ((x + 1) * settings.GRID_SPACING))

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
