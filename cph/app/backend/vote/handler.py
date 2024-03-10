import logging

from hearthstone.entities import Card

from cph.resources import card_names
from cph.game import handler
from cph.game.model import GameOption

from .model import VoteOption
from .controller import VoteController


EMOTE_OPTIONS = [
    GameOption(option=emote, group='Misc', suboptions=[])
    for emote in ('Greetings', 'Well Played', 'Thanks', 'Wow', 'Oops', 'Threaten')
]


class VoteHandler(handler.Handler):
    def __init__(self, voteController: VoteController, logger: logging.Logger):
        self._voteController = voteController
        self._voteModel = voteController._voteModel
        self._logger = logger
        self._card_names = card_names.load()

        self._prev_cards: list[Card] = []
        self._game_options: list[GameOption] = []

    def _card_name(self, card: Card) -> str:
        key = card.card_id if card.card_id is not None else ''
        return self._card_names.get(key, f'UNKNOWN: {card.card_id}')

    def _set_game_options(self, game_options: list[GameOption]):
        vote_options = [
            VoteOption(
                option=game_option.option,
                alias=game_option.make_alias(index),
                votes=0,
            )
            for index, game_option in enumerate(game_options)
        ]
        self._game_options = game_options
        self._voteModel.set_options(game_options, vote_options)

    def set_options(self, options: list[Card], options_targets: list[list[Card]]):
        if len(options) == 0 or self._prev_cards == options:
            return
        self._prev_cards = options

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
        game_options.append(GameOption(option='End Turn',
                            group='Misc', suboptions=[]))
        if self._voteController._voteEmotes:
            game_options.append(GameOption(
                option='Emote', group='Misc', suboptions=EMOTE_OPTIONS))
        self._set_game_options(game_options)

    def set_choices(self, choices: list[Card], max_count: int):
        # TODO: handle max_count
        game_options = [
            GameOption(
                option=self._card_name(choice),
                group='Choice',
                suboptions=[]
            )
            for choice in choices
        ]
        self._set_game_options(game_options)

    def clear(self):
        self._prev_cards.clear()
        self._voteModel.set_options([], [])

    def on_selected_option(self, index: int):
        if index < 0 or index >= len(self._game_options):
            self.clear()
            return
        suboptions = self._game_options[index].suboptions
        self._set_game_options(suboptions)
