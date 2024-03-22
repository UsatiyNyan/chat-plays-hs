import logging

from hearthstone.entities import Card

from .board import Board


class Handler:
    def __init__(self, logger: logging.Logger):
        self._logger = logger

    def set_options(self, board: Board, options: list[Card], options_targets: list[list[Card]]):
        self._logger.debug(f'[handler][options] {board=}')
        for option, targets in zip(options, options_targets):
            self._logger.debug(f'[handler][option] {option} -> {targets}')

    def set_choices(self, choices: list[Card], max_count: int):
        self._logger.debug(f'[handler][choices] {choices} max={max_count}')

    def clear(self):
        self._logger.debug('clear')
