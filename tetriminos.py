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

        self._draw()

    def __getstate__(self):
        """Needed by Pickle to give the proper attributes to be picked."""
        state = self.__dict__.copy()

        del state['image']
        del state['rect']

        return state

    def __setstate__(self, state):
        """Needed by Pickle to properly initialize this Block instance."""
        self.__dict__.update(state)

        self._draw()

    def _draw(self):
        """Draw this Block object."""
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
        self._draw(x, y)

    def _draw(self, x, y):
        """Draw the blocks of this Tetrimino."""
        self.blocks = []

        for pat_y, y_val in enumerate(self.pattern):
            for pat_x, x_val in enumerate(self.pattern[pat_y]):
                if self.pattern[pat_y][pat_x] != 1:
                    continue

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

    def get_top_left_pos(self):
        """Return the position of the top-left-most block of this Tetrimino."""
        left_most_x = settings.COLS - 1
        top_most_y = settings.ROWS - 1

        for block in self.blocks:
            if block.x < left_most_x:
                left_most_x = block.x

            if block.y < top_most_y:
                top_most_y = block.y

        return left_most_x, top_most_y

    def rotate(self, fallen_blocks):
        """Rotates this Tetrimino by 90 degrees clockwise."""
        left_most_block_x, top_most_block_y = self.get_top_left_pos()

        # Rotate the pattern of this Tetrimino by 90 degress clockwise
        new_pattern = list(zip(*self.pattern[::-1]))

        new_pattern_height = len(new_pattern)
        new_pattern_width = len(new_pattern[0])

        # Check if the new position of all the blocks will collide with others or will go outside the playground
        for pat_y, y_val in enumerate(new_pattern):
            for pat_x, x_val in enumerate(new_pattern[pat_y]):
                if new_pattern[pat_y][pat_x] != 1:
                    continue

                new_x = left_most_block_x + pat_x
                new_y = top_most_block_y + pat_y

                if new_x < 0:
                    left_most_block_x = 0

                if new_x > settings.COLS - 1:
                    left_most_block_x = (settings.COLS - 1) - (new_pattern_width - 1)

                if new_y < 0:
                    top_most_block_y = 0

                if new_y > settings.ROWS - 1:
                    top_most_block_y = (settings.ROWS - 1) - (new_pattern_height - 1)

                new_x = left_most_block_x + pat_x
                new_y = top_most_block_y + pat_y

                # Check if the new block is colliding with an already fallen one. If yes, abort the rotating operation
                for fallen_block in fallen_blocks:
                    if fallen_block.x == new_x and fallen_block.y == new_y:
                        return False

        # If there'll not be any issue while rotating this Tetrimino: erase the old pattern as well as the old blocks
        self.pattern = new_pattern
        self._draw(left_most_block_x, top_most_block_y)

        return True

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
        [1, 1]
    ]


class LTetrimino(Tetrimino):
    background_color = (255, 165, 0)
    pattern = [
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
