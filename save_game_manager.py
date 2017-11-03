import logging
import pickle
import os


def load_game(filename, obj, attrs):
    """Load a saved game."""
    if not os.path.isfile(filename):
        logging.info('Save file does not exists')
        return

    logging.info('Loading saved game')

    with open(filename, 'rb') as f:
        data = pickle.load(f)

    for attr in attrs:
        if attr in data:
            setattr(obj, attr, data[attr])


def save_game(filename, obj, attrs):
    """Save the current game."""
    logging.info('Saving current game')

    data = {}

    for attr in attrs:
        data[attr] = getattr(obj, attr)

    with open(filename, 'wb') as f:
        pickle.dump(data, f)
