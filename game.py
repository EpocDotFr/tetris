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
        self.blocks = []
        self.current_tetrimino = None

        self.blocks.append(tetriminos.Block((200, 200, 200), 1, 1))
        self.blocks.append(tetriminos.Block((200, 200, 200), 0, 1))
        self.blocks.append(tetriminos.Block((200, 200, 200), 0, 0))
        self.blocks.append(tetriminos.Block((200, 200, 200), 0, 4))

        pygame.time.set_timer(settings.TETRIMINOS_FALLING_EVENT, settings.TETRIMINOS_FALLING_INTERVAL)

    def _set_current_tetrimino(self):
        if self.current_tetrimino:
            return

        self.current_tetrimino = getattr(tetriminos, random.choice(tetriminos.__all__))()

    def update(self):
        # self._set_current_tetrimino()

        # ----------------------------------------------------------------------
        # Events handling

        for event in pygame.event.get():
            self._event_quit(event)
            # self._event_falling_tetrimino(event)
            # self._event_game_key(event)

        # ----------------------------------------------------------------------
        # Drawing

        self.window.fill((255, 255, 255))

        self._draw_grid()
        self._draw_blocks()

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

        if self.current_tetrimino.rect.bottom + settings.BLOCKS_SIDE_SIZE + settings.GRID_SPACING > self.window_rect.h:
            self.current_tetrimino = None
        else:
            self.current_tetrimino.rect.bottom += settings.BLOCKS_SIDE_SIZE + settings.GRID_SPACING

    def _event_game_key(self, event):
        if event.type != pygame.KEYDOWN:
            return

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

    def _draw_grid(self):
        if settings.DRAW_GRID:
            for x in range(1, settings.COLS):
                pos = pygame.Rect((x * settings.BLOCKS_SIDE_SIZE + (x - 1) * settings.GRID_SPACING, 0), (settings.GRID_SPACING, self.window_rect.h))

                pygame.draw.rect(self.window, settings.GRID_COLOR, pos)

            for y in range(1, settings.ROWS):
                pos = pygame.Rect((0, y * settings.BLOCKS_SIDE_SIZE + (y - 1) * settings.GRID_SPACING), (self.window_rect.w, settings.GRID_SPACING))

                pygame.draw.rect(self.window, settings.GRID_COLOR, pos)

    def _draw_blocks(self):
        for block in self.blocks:
            block.rect.top = block.y * settings.BLOCKS_SIDE_SIZE + block.y * settings.GRID_SPACING
            block.rect.left = block.x * settings.BLOCKS_SIDE_SIZE + block.x * settings.GRID_SPACING

            self.window.blit(block.image, block.rect)
