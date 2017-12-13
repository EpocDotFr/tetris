import pygame
import math
import sys
import os

# ----------------------------------------------------------------------
# Editable settings

FPS = 30
BLOCKS_SIDE_SIZE = 20
SAVE_FILE_NAME = 'save.dat'
STATS_FILE_NAME = 'stats.json'
TETRIMINOS_INITIAL_FALLING_INTERVAL = 1000
TETRIMINOS_FALLING_INTERVAL_DECREASE_STEP = 100
TETRIMINOS_FAST_FALLING_INTERVAL = 50
LEVEL_INCREASE_LINES_STEP = 8
COMPLETED_LINE_SCORE = 10

COLS = 12
ROWS = 30

DRAW_GRID = True
GRID_SPACING = 1
GRID_COLOR = (255, 255, 255)

WINDOW_BACKGROUND_COLOR = (218, 235, 252)
PLAYGROUND_BACKGROUND_COLOR = (190, 207, 234)
TEXT_COLOR = (113, 130, 165)

MUSIC_VOLUME = 0.2
SOUNDS_VOLUME = 0.3

# ----------------------------------------------------------------------
# Game constants - do not edit anything after this line

# When frozen by PyInstaller, the path to the resources is different
RESOURCES_ROOT = os.path.join(sys._MEIPASS, 'resources') if getattr(sys, 'frozen', False) else 'resources'

TETRIMINOS_FALLING_EVENT = pygame.USEREVENT + 1
GAME_DURATION_EVENT = pygame.USEREVENT + 2


class GameState:
    PLAYING = 2
    PAUSED = 4
    GAME_OVER = 8
    SHOW_STATS = 16

INFO_PANEL_WIDTH = 150

PLAYGROUND_WIDTH = COLS * BLOCKS_SIDE_SIZE + (COLS - 1) * GRID_SPACING
PLAYGROUND_HEIGHT = ROWS * BLOCKS_SIDE_SIZE + (ROWS - 1) * GRID_SPACING
PLAYGROUND_CENTERX = math.floor((COLS - 1) / 2)

WINDOW_SIZE = (
    PLAYGROUND_WIDTH + INFO_PANEL_WIDTH,
    PLAYGROUND_HEIGHT
)
