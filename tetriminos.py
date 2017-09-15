import settings
import pygame


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

        self._init()

    def __getstate__(self):
        """Needed by Pickle to give the proper attributes to be picked."""
        state = self.__dict__.copy()

        del state['image']
        del state['rect']

        return state

    def __setstate__(self, state):
        """Needed by Pickle to properly initialize this Block instance."""
        self.__dict__.update(state)

        self._init()

    def _init(self):
        """Initialize this Block object."""
        self.image = pygame.Surface((settings.BLOCKS_SIDE_SIZE, settings.BLOCKS_SIDE_SIZE), pygame.SRCALPHA, 32).convert_alpha()
        self.image.fill(self.background_color)

        self.rect = self.image.get_rect()

    def will_collide(self, fallen_blocks, direction=(0, 0)):
        """Check if this block is about to collide with other blocks in the specified direction."""
        new_x = self.x + direction[0]
        new_y = self.y + direction[1]

        for fallen_block in fallen_blocks:
            if fallen_block.x == new_x and fallen_block.y == new_y:
                return True

        return False

    def is_bottommost(self):
        """Check if this block is on the bottommost of the playground."""
        if self.y == settings.ROWS - 1:
            return True

        return False

    def is_leftmost(self):
        """Check if this block is on the leftmost of the playground."""
        if self.x == 0:
            return True

        return False

    def is_rightmost(self):
        """Check if this block is on the rightmost of the playground."""
        if self.x == settings.COLS - 1:
            return True

        return False


class Tetrimino:
    def __init__(self, x, y):
        self._init(x, y)

    def _init(self, x, y):
        """Build the blocks of this Tetrimino."""
        self.blocks = []

        for pat_y, y_val in enumerate(self.pattern):
            for pat_x, x_val in enumerate(self.pattern[pat_y]):
                if self.pattern[pat_y][pat_x] == 1:
                    self.blocks.append(Block(self.background_color, x + pat_x, y + pat_y))

    def make_it_fall(self, fallen_blocks):
        """Makes this Tetrimino to fall."""
        if self.is_bottommost() or self.will_collide(fallen_blocks, (0, 1)):
            return False

        for block in self.blocks:
            block.y += 1

        return True

    def move_left(self, fallen_blocks):
        """Moves this Tetrimino to the left."""
        if self.is_leftmost() or self.will_collide(fallen_blocks, (-1, 0)):
            return False

        for block in self.blocks:
            block.x -= 1

        return True

    def move_right(self, fallen_blocks):
        """Moves this Tetrimino to the right."""
        if self.is_rightmost() or self.will_collide(fallen_blocks, (1, 0)):
            return False

        for block in self.blocks:
            block.x += 1

        return True

    def rotate(self, fallen_blocks):
        """Rotates this Tetrimino by 90 degrees clockwise."""
        # Get the position of the top-left-most block of this Tetrimino. This will be our reference position on the
        # playground for all rotation operations
        top_left_most_block_x = settings.COLS - 1
        top_left_most_block_y = settings.ROWS - 1

        for block in self.blocks:
            if block.x < top_left_most_block_x and block.y < top_left_most_block_y:
                top_left_most_block_x = block.x
                top_left_most_block_y = block.y

        # Rotate the pattern of this Tetrimino by 90 degress clockwise
        new_pattern = list(zip(*self.pattern[::-1]))

        # Check if the new position of all the blocks will collide with others or with the playground edges
        for pat_y, y_val in enumerate(new_pattern):
            for pat_x, x_val in enumerate(new_pattern[pat_y]):
                if new_pattern[pat_y][pat_x] == 1:
                    new_x = top_left_most_block_x + pat_x
                    new_y = top_left_most_block_y + pat_y

                    # Check if the new bloc is colliding with an already fallen one
                    for fallen_block in fallen_blocks:
                        if fallen_block.x == new_x and fallen_block.y == new_y:
                            return # Abort the rotating operation if one block is colliding with an already fallen one

        self.pattern = new_pattern # Erase the old pattern by the new one
        self._init(top_left_most_block_x, top_left_most_block_y) # Erase the old blocks by the new ones

    def will_collide(self, fallen_blocks, direction=(0, 0)):
        """Check if this Tetrimino is about to collide with other blocks in the specified direction."""
        for block in self.blocks:
            if block.will_collide(fallen_blocks, direction):
                return True

        return False

    def is_bottommost(self):
        """Check if this Tetrimino is on the bottommost of the playground."""
        for block in self.blocks:
            if block.is_bottommost():
                return True

        return False

    def is_leftmost(self):
        """Check if this Tetrimino is on the leftmost of the playground."""
        for block in self.blocks:
            if block.is_leftmost():
                return True

        return False

    def is_rightmost(self):
        """Check if this Tetrimino is on the rightmost of the playground."""
        for block in self.blocks:
            if block.is_rightmost():
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
