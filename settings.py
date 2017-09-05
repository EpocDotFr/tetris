import pygame
import os
import sys


FPS = 30
BLOCKS_SIDE_SIZE = 25
COLS = 12
ROWS = 30
DRAW_GRID = True
GRID_SPACING = 1
GRID_COLOR = (225, 225, 225)

# When frozen by PyInstaller, the path to the resources is different
RESOURCES_ROOT = os.path.join(sys._MEIPASS, 'resources') if getattr(sys, 'frozen', False) else 'resources'

TETRIMINOS_FALLING_EVENT = pygame.USEREVENT + 1
TETRIMINOS_FALLING_INTERVAL = 1000
