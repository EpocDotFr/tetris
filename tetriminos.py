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


class BasicPos:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class AdvancedPos(BasicPos):
    def __init__(self, x, y):
        super(AdvancedPos, self).__init__(x, y)

        self.top = None # TODO
        self.left = None # TODO
        self.bottom = None # TODO
        self.right = None # TODO


class Block(pygame.sprite.Sprite):
    def __init__(self, background_color, pos):
        super(Block, self).__init__()

        self.background_color = background_color
        self.pos = pos

        self.image = pygame.Surface((settings.BLOCKS_SIDE_SIZE, settings.BLOCKS_SIDE_SIZE), pygame.SRCALPHA, 32).convert_alpha()
        self.image.fill(self.background_color)

        self.rect = self.image.get_rect()


class Tetrimino:
    def __init__(self):
        self.rows = len(self.pattern)
        self.cols = len(self.pattern[0])

        self.pos = AdvancedPos(3, 0) # TODO Place at the center of the well

        self._init_blocks()

    def make_it_fall(self):
        if self._is_bottommost():
            return False

        self.pos.y += 1

        for block in self.blocks:
            block.pos.y += 1

        return True

    def move_left(self):
        if self._is_leftmost():
            return False

        self.pos.x -= 1

        for block in self.blocks:
            block.pos.x -= 1

        return True

    def move_right(self):
        if self._is_rightmost():
            return False

        self.pos.x += 1

        for block in self.blocks:
            block.pos.x += 1

        return True

    def drop(self):
        pass

    def rotate(self):
        self.pattern = list(zip(*self.pattern[::-1]))

        self._init_blocks()

    def _init_blocks(self):
        self.blocks = []

        for x, x_val in enumerate(self.pattern):
            for y, y_val in enumerate(self.pattern[x]):
                if self.pattern[x][y] == 1:
                    block = Block(self.background_color, BasicPos(self.pos.x + x, self.pos.y + y))

                    self.blocks.append(block)

    def _is_bottommost(self):
        return self.pos.y == 2
        return False # TODO

    def _is_leftmost(self):
        return False # TODO

    def _is_rightmost(self):
        return False # TODO


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
