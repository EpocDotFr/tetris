import logging
import pygame
import game
import sys
import os


def run():
    if 'SDL_VIDEO_WINDOW_POS' not in os.environ:
        os.environ['SDL_VIDEO_CENTERED'] = '1' # This makes the window centered on the screen

    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%d/%m/%Y %H:%M:%S',
        stream=sys.stdout
    )

    logging.getLogger().setLevel(logging.INFO)

    logging.info('Initializing PyGame/{} (with SDL/{})'.format(
        pygame.version.ver,
        '.'.join(str(v) for v in pygame.get_sdl_version())
    ))

    pygame.mixer.pre_init(0, 0, 4, 2048) # Zeros makes PyGame to use default values
    pygame.init()

    logging.info('Initializing game')

    g = game.Game()

    logging.info('Running game')

    while True:
        g.update()


if __name__ == '__main__':
    run()
