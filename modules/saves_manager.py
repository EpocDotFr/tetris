
import settings
import logging
import pickle
import os


class SavesManager:
    save_data = [
        'fallen_blocks',
        'level',
        'lines',
        'score',
        'current_tetrimino',
        'next_tetrimino'
    ]

    def __init__(self, game):
        self.game = game

    def load_game(self):
        """Load a saved game."""
        if not os.path.isfile(settings.SAVE_FILE_NAME):
            logging.info('Save file does not exists')
            return

        logging.info('Loading saved game')

        with open(settings.SAVE_FILE_NAME, 'rb') as f:
            data = pickle.load(f)

        for sd in self.save_data:
            if sd in data:
                setattr(self.game, sd, data[sd])

        self.game.is_paused = False
        self.game.is_game_over = False

        self.game._enable_or_update_falling_interval()

    def save_game(self):
        """Save the current game."""
        if self.game.is_game_over:
            return

        logging.info('Saving current game')

        data = {}

        for sd in self.save_data:
            data[sd] = getattr(self.game, sd)

        with open(settings.SAVE_FILE_NAME, 'wb') as f:
            pickle.dump(data, f)
