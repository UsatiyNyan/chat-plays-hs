import typing as t
import logging

from hearthstone.entities import Card


class GameState:
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def set_options(self, options: list[Card], options_targets: list[list[Card]]):
        for option, targets in zip(options, options_targets):
            self.logger.debug(f'option: {option} -> {targets}')

    def set_choices(self, choices: list[Card], max_count: int, is_mulligan: bool):
        if is_mulligan and max_count > 3:
            choices = \
                list(filter(lambda x: x.card_id and 'COIN' not in x.card_id, choices))
            max_count = min(max_count, len(choices))
        self.logger.debug(f'max={max_count} choices={choices}')

    def clear(self):
        self.logger.debug('clear')
