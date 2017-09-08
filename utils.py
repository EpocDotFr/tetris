from random import choice
import settings
import pygame
import os


def _get_resource_path(res_type, filename):
    """Get the path to a resource."""
    path = os.path.join(settings.RESOURCES_ROOT, res_type, filename)

    if not os.path.isfile(path):
        raise ValueError('The file ' + path + ' doesn\'t exist')

    return path


def load_image(filename):
    """Load an image."""
    path = _get_resource_path('images', filename)

    return pygame.image.load(path).convert_alpha()


def load_sound(filename, volume=0.5):
    """Load a sound effect."""
    if volume == 0:
        return

    path = _get_resource_path('sounds', filename)

    sound = pygame.mixer.Sound(file=path)
    sound.set_volume(volume)

    return sound


def load_music(filename, play=True, volume=0.5):
    """Load a music track."""
    if volume == 0:
        return

    path = _get_resource_path('musics', filename)

    pygame.mixer.music.load(path)
    pygame.mixer.music.set_volume(volume)

    if play:
        pygame.mixer.music.play(-1)


def load_random_music(filenames, play=True, volume=0.5):
    """Randomly load a music track from a list."""
    load_music(choice(filenames), play, volume)


def load_font(filename, size):
    """Load a font file."""
    path = _get_resource_path('fonts', filename)

    return pygame.font.Font(path, size)
