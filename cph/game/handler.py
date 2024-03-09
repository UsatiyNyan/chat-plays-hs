import logging

from hearthstone.entities import Card


class Handler:
    def set_options(self, options: list[Card], options_targets: list[list[Card]]):
        pass

    def set_choices(self, choices: list[Card], max_count: int):
        pass

    def clear(self):
        pass


class LoggingHandler(Handler):
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def set_options(self, options: list[Card], options_targets: list[list[Card]]):
        for option, targets in zip(options, options_targets):
            self.logger.debug(f'option: {option} -> {targets}')

    def set_choices(self, choices: list[Card], max_count: int):
        self.logger.debug(f'max={max_count} choices={choices}')

    def clear(self):
        self.logger.debug('clear')
