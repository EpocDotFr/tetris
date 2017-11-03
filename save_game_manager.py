import logging
import pickle


def load_game(filename, object, attributes):
    """Load a saved game."""
    logging.info('Loading saved game')

    with open(filename, 'rb') as f:
        data = pickle.load(f)

    for attr in attributes:
        if attr in data:
            setattr(object, attr, data[attr])


def save_game(filename, object, attributes):
    """Save the current game."""
    logging.info('Saving current game')

    data = {}

    for attr in attributes:
        data[attr] = getattr(object, attr)

    with open(filename, 'wb') as f:
        pickle.dump(data, f)
