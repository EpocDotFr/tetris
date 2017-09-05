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
    def __init__(self, background_color, pos_x, pos_y):
        super(Block, self).__init__()

        self.background_color = background_color
        self.pos_x = pos_x
        self.pos_y = pos_y

        self.image = pygame.Surface((settings.BLOCKS_SIDE_SIZE, settings.BLOCKS_SIDE_SIZE), pygame.SRCALPHA, 32).convert_alpha()
        self.image.fill(self.background_color)

        self.rect = self.image.get_rect()


class Tetrimino:
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y

        self.blocks = []

        for x, x_val in enumerate(self.pattern):
            for y, y_val in enumerate(self.pattern[x]):
                if self.pattern[x][y] == 1:
                    block = Block(self.background_color, self.pos_x + x, self.pos_y + y)

                    self.blocks.append(block)

    def rotate(self):
        prev_post = self.rect.topleft

        self.pattern = list(zip(*self.pattern[::-1]))
        self.image = pygame.transform.rotate(self.image, -90)
        self.rect = self.image.get_rect()
        self.rect.topleft = prev_post


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
