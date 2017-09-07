import pygame
import os
import sys

# ----------------------------------------------------------------------
# Editable settings

FPS = 30
BLOCKS_SIDE_SIZE = 20

COLS = 12
ROWS = 30

DRAW_GRID = True
GRID_SPACING = 1
GRID_COLOR = (218, 235, 252)

WINDOW_BACKGROUND_COLOR = (218, 235, 252)
PLAYGROUND_BACKGROUND_COLOR = (190, 207, 234)

TEXT_DARK_COLOR = (113, 130, 165)
TEXT_LIGHT_COLOR = (151, 173, 219)

# ----------------------------------------------------------------------
# Game constants - do not edit

# When frozen by PyInstaller, the path to the resources is different
RESOURCES_ROOT = os.path.join(sys._MEIPASS, 'resources') if getattr(sys, 'frozen', False) else 'resources'

TETRIMINOS_FALLING_EVENT = pygame.USEREVENT + 1
TETRIMINOS_FALLING_INTERVAL = 1000

INFO_PANEL_WIDTH = 150

PLAYGROUND_WIDTH = COLS * BLOCKS_SIDE_SIZE + (COLS - 1) * GRID_SPACING
PLAYGROUND_HEIGHT = ROWS * BLOCKS_SIDE_SIZE + (ROWS - 1) * GRID_SPACING

WINDOW_SIZE = (
    PLAYGROUND_WIDTH + INFO_PANEL_WIDTH,
    PLAYGROUND_HEIGHT
)
