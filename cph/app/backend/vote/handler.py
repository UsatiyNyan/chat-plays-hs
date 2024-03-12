import logging

from hearthstone.entities import Card

from cph.resources import card_names
from cph.game import handler

from cph.game.model import GameOption

from .controller import VoteController


EMOTE_OPTIONS = [
    GameOption(option=emote, group='Misc', suboptions=[])
    for emote in ('Greetings', 'Well Played', 'Thanks', 'Wow', 'Oops', 'Threaten')
]


class VoteHandler(handler.Handler):
    def __init__(self,
                 voteController: VoteController,
                 logger: logging.Logger):
        self._controller = voteController

        self._logger = logger
        self._card_names = card_names.load()

        self._prev_cards: list[Card] = []

    def _check_prev_cards(self, cards: list[Card]) -> bool:
        if self._prev_cards == cards:
            return False
        self._prev_cards = cards
        return True

    def _card_name(self, card: Card) -> str:
        key = card.card_id if card.card_id is not None else ''
        return self._card_names.get(key, f'UNKNOWN: {card.card_id}')

    def set_options(self, options: list[Card], options_targets: list[list[Card]]):
        if self._controller.is_busy or not self._check_prev_cards(options):
            return

        game_options = [
            GameOption(
                option=self._card_name(option),
                group=GameOption.make_group(option.zone),
                suboptions=[
                    GameOption(
                        option=self._card_name(target),
                        group='Target',
                        suboptions=[],
                    )
                    for target in targets
                ]
            )
            for option, targets in zip(options, options_targets)
        ]
        game_options.append(
            GameOption(option='End Turn', group='Misc', suboptions=[]))
        if self._controller.voteEmotes:
            game_options.append(
                GameOption(option='Emote', group='Misc', suboptions=EMOTE_OPTIONS))

        self._controller.set_game_options(game_options)

    def set_choices(self, choices: list[Card], max_count: int):
        if self._controller.is_busy or not self._check_prev_cards(choices):
            return

        game_options = [
            GameOption(
                option=self._card_name(choice),
                group='Choice',
                suboptions=[]
            )
            for choice in choices
        ]

        self._controller.set_game_options(game_options, max_count)

    def clear(self):
        if self._controller.is_busy or not self._check_prev_cards([]):
            return
        self._controller.set_game_options([])
