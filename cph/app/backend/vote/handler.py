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

    def _card_name(self, card: Card) -> str:
        return self._card_names.get(card.card_id, f'UNKNOWN: {card.card_id}')

    def set_options(self, options: list[Card], options_targets: list[list[Card]]):
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

        if len(game_options) == 0:
            return

        game_options.append(GameOption(option='End Turn',
                            group='Misc', suboptions=[]))
        if self._voteController._voteEmotes:
            game_options.append(GameOption(
                option='Emote', group='Misc', suboptions=EMOTE_OPTIONS))

        vote_options = [
            VoteOption(
                option=game_option.option,
                alias=game_option.make_alias(index),
                votes=0,
            )
            for index, game_option in enumerate(game_options)
        ]
        self._voteModel.set_options(game_options, vote_options)
        for option, targets in zip(options, options_targets):
            self._logger.debug(f'option: {option} -> {targets}')

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
        vote_options = [
            VoteOption(
                option=game_option.option,
                alias=game_option.make_alias(index),
                votes=0,
            )
            for index, game_option in enumerate(game_options)
        ]
        self._voteModel.set_options(game_options, vote_options)
        self._logger.debug(f'choices={choices} max={max_count}')

    def clear(self):
        self._voteModel.set_options([], [])
