import logging

from hearthstone.entities import Card

from cph.resources import card_names
from cph.game import handler

from cph.game.model import GameOption
from cph.vote.model import VoteOption

from cph.vote.machine import VoteMachine

from .controller import VoteController


EMOTE_OPTIONS = [
    GameOption(option=emote, group='Misc', suboptions=[])
    for emote in ('Greetings', 'Well Played', 'Thanks', 'Wow', 'Oops', 'Threaten')
]


class VoteHandler(handler.Handler):
    def __init__(self,
                 voteController: VoteController,
                 vote_machine: VoteMachine,
                 logger: logging.Logger):
        self._controller = voteController
        self._controller.on_vote_button_clicked = self.on_vote_button_clicked
        self._model = voteController._voteModel

        self._machine = vote_machine
        self._machine.on_update_votes = self.on_update_votes
        self._machine.on_selected_winners = self.on_selected_winners
        self._machine.on_proceed_with_option = self.on_proceed_with_option

        self._logger = logger
        self._card_names = card_names.load()

        self._prev_cards: list[Card] = []
        self._game_options: list[GameOption] = []

    def _check_prev_cards(self, cards: list[Card]) -> bool:
        if self._prev_cards == cards:
            return False
        self._prev_cards = cards
        return True

    def _card_name(self, card: Card) -> str:
        key = card.card_id if card.card_id is not None else ''
        return self._card_names.get(key, f'UNKNOWN: {card.card_id}')

    def _set_game_options(self, game_options: list[GameOption], max_count: int = 1):
        vote_options = [
            VoteOption(
                option=game_option.option,
                alias=game_option.make_alias(index),
                votes=0,
            )
            for index, game_option in enumerate(game_options)
        ]
        self._game_options = game_options
        self._model.set_options(game_options, vote_options)
        self._machine.set_options(vote_options, max_count)

    def set_options(self, options: list[Card], options_targets: list[list[Card]]):
        if self._machine.is_busy or not self._check_prev_cards(options):
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
        self._set_game_options(game_options)

    def set_choices(self, choices: list[Card], max_count: int):
        if self._machine.is_busy or not self._check_prev_cards(choices):
            return

        game_options = [
            GameOption(
                option=self._card_name(choice),
                group='Choice',
                suboptions=[]
            )
            for choice in choices
        ]
        self._set_game_options(game_options, max_count)

    def clear(self):
        if self._machine.is_busy or not self._check_prev_cards([]):
            return
        self._set_game_options([])

    def on_vote_button_clicked(self):
        self._machine.on_vote_button_clicked(self._controller.voteSecondsTotal)

    def on_update_votes(self, vote_options: list[VoteOption]):
        self._model.update_votes(vote_options)

    def on_selected_winners(self, indices: list[int]):
        self._controller.voteWinnerIndices = indices

    def on_proceed_with_option(self, index: int):
        if index < 0 or index >= len(self._game_options):
            self._logger.error(f'selected_option invalid index: {index}')
            return
        suboptions = self._game_options[index].suboptions
        self._set_game_options(suboptions)
