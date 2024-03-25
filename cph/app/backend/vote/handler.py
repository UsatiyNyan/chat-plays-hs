import logging

from hearthstone.entities import Card
from hearthstone.enums import GameTag, CardType, Zone

from cph.resources import card_names
from cph.game import handler
from cph.game.board import Board

from cph.game.model import GameOption

from .controller import VoteController
from .misc import END_TURN_OPTION, make_suboptions, make_deck_option


class VoteHandler(handler.Handler):
    def __init__(self,
                 voteController: VoteController,
                 logger: logging.Logger):
        super().__init__(logger)
        self._controller = voteController
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

    def set_options(self, board: Board, options: list[Card], options_targets: list[list[Card]]):
        if self._controller.is_busy or not self._check_prev_cards(options):
            return

        game_options: list[GameOption] = []

        for option, targets in zip(options, options_targets):
            if len(targets) == 1 and targets[0].id == option.id and \
                (option.tags.get(GameTag.TRADEABLE) is not None or
                 option.tags.get(GameTag.FORGE) is not None):
                game_options.append(make_deck_option(option, self._card_name))
            else:
                game_options.append(
                    GameOption(
                        option=self._card_name(option),
                        group=GameOption.make_group(option.zone),
                        entity_id=option.id,
                        card_type=CardType(option.type),
                        zone=Zone(option.zone),
                        zone_pos=option.tags.get(GameTag.ZONE_POSITION, 0),
                        suboptions=make_suboptions(board, option, targets, self._card_name))
                )

        game_options.append(END_TURN_OPTION)

        self._controller.set_game_options(board, game_options)

    def set_choices(self, choices: list[Card], max_count: int):
        if self._controller.is_busy or not self._check_prev_cards(choices):
            return

        game_options = [
            GameOption(
                option=self._card_name(choice),
                group='Choice',
                entity_id=choice.id,
                card_type=CardType(choice.type),
                zone=Zone(choice.zone),
                zone_pos=choice.tags.get(GameTag.ZONE_POSITION, 0),
                suboptions=[]
            )
            for choice in choices
        ]

        self._controller.set_game_options(None, game_options, max_count)

    def clear(self):
        if self._controller.is_busy:
            return
        pass
