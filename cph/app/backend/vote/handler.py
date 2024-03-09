import logging

from hearthstone.entities import Card

from cph.game import handler
from cph.game.model import GameOption, load_card_names

from .model import VoteOption
from .controller import VoteController


class VoteHandler(handler.Handler):
    def __init__(self, voteController: VoteController, logger: logging.Logger):
        self._voteController = voteController
        self._voteModel = voteController._voteModel
        self._logger = logger
        self._card_names = load_card_names()

    def set_options(self, options: list[Card], options_targets: list[list[Card]]):
        game_options = [
            GameOption(
                option=self._card_names.get(option.card_id, option.card_id),
                group=GameOption.make_group(option.zone),
                suboptions=[
                    GameOption(
                        option=self._card_names.get(target.card_id, target.card_id),
                        group='Target',
                        suboptions=[],
                    )
                    for target in targets
                ]
            )
            for option, targets in zip(options, options_targets)
        ]
        # TODO: add emotes, end turn 'Misc' group
        vote_options = [
            VoteOption(
                option=game_option.option,
                alias=game_option.make_alias(index),
                votes=0,
            )
            for index, game_option in enumerate(game_options)
        ]
        self._voteModel.set_options(game_options, vote_options)

    def set_choices(self, choices: list[Card], max_count: int):
        game_options = [
            GameOption(
                option=self._card_names.get(choice.card_id, choice.card_id),
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

    def clear(self):
        self._voteModel.set_options([], [])
