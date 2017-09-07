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


class Tetrimino:
    def __init__(self, x, y):
        self.rows = len(self.pattern)
        self.cols = len(self.pattern[0])

        self.blocks = []

        for pat_y, y_val in enumerate(self.pattern):
            for pat_x, x_val in enumerate(self.pattern[pat_y]):
                if self.pattern[pat_y][pat_x] == 1:
                    self.blocks.append(Block(self.background_color, x + pat_x, y + pat_y))

    def make_it_fall(self):
        if self._is_bottommost():
            return False

        for block in self.blocks:
            block.y += 1

        return True

    def move_left(self):
        if self._is_leftmost():
            return False

        for block in self.blocks:
            block.x -= 1

        return True

    def move_right(self):
        if self._is_rightmost():
            return False

        for block in self.blocks:
            block.x += 1

        return True

    def drop(self):
        pass

    def rotate(self):
        pass

    def _is_bottommost(self):
        for block in self.blocks:
            if block.y == settings.ROWS - 1:
                return True

        return False

    def _is_leftmost(self):
        for block in self.blocks:
            if block.x == 0:
                return True

        return False

    def _is_rightmost(self):
        for block in self.blocks:
            if block.x == settings.COLS - 1:
                return True

        return False


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
