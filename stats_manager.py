import logging
import json
import os


def load_stats(filename, stats_dict):
    """Save the current stats to a JSON file."""
    if not os.path.isfile(filename):
        logging.info('Stats file does not exists')
        return

    logging.info('Loading stats')

    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

        for key, value in data.items():
            stats_dict[key]['value'] = value


def save_stats(filename, stats_dict):
    """Load stats from a JSON file."""
    logging.info('Saving stats')

    data = {}

    for key, stat in stats_dict.items():
        data[key] = stat['value']

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f)
