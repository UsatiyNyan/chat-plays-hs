import typing as t

from hearthstone.entities import Card
from hearthstone.enums import GameTag, CardType, Zone

from cph.game.model import GameOption
from cph.game.board import Board

MISC_GROUP = 'Misc'
TARGET_GROUP = 'Target'
POSITION_GROUP = 'Position'

EMOTE_OPTION_NAME = 'Emote'
EMOTE_SUBOPTIONS = (
    'Greetings', 'Well Played', 'Thanks', 'Wow', 'Oops', 'Threaten'
)

END_TURN_OPTION_NAME = 'End Turn'
END_TURN_OPTION = GameOption(
    option=END_TURN_OPTION_NAME,
    group=MISC_GROUP,
    entity_id=0,
    card_type=CardType.INVALID,
    zone=Zone.INVALID,
    zone_pos=0,
    suboptions=[]
)

ANYWHERE_OPTION_NAME = 'Anywhere'
ANYWHERE_OPTION = GameOption(
    option='Anywhere',
    group=POSITION_GROUP,
    entity_id=0,
    card_type=CardType.INVALID,
    zone=Zone.PLAY,
    zone_pos=0,
    suboptions=[]
)

DECK_OPTION_NAME = 'Deck'
DECK_OPTION = GameOption(
    option=DECK_OPTION_NAME,
    group=TARGET_GROUP,
    entity_id=0,
    card_type=CardType.INVALID,
    zone=Zone.DECK,
    zone_pos=0,
    suboptions=[]
)


def _make_emote_option(suboptions: list[GameOption]):
    return [
        GameOption(
            option=emote,
            group=MISC_GROUP,
            entity_id=0,
            card_type=CardType.INVALID,
            zone=Zone.INVALID,
            zone_pos=index + 1,
            suboptions=suboptions,
        )
        for index, emote in enumerate(EMOTE_SUBOPTIONS)
    ]


def add_emote_option(game_options: list[GameOption]):
    if len(game_options) == 0:
        return
    last_option = game_options[-1]
    if last_option.option == END_TURN_OPTION_NAME and \
            last_option.group == MISC_GROUP:
        game_options.append(GameOption(
            option=EMOTE_OPTION_NAME,
            group=MISC_GROUP,
            entity_id=0,
            card_type=CardType.INVALID,
            zone=Zone.INVALID,
            zone_pos=0,
            suboptions=_make_emote_option(game_options)
        ))


def remove_emote_option(game_options: list[GameOption]):
    if len(game_options) == 0:
        return
    last_option = game_options[-1]
    if last_option.option == EMOTE_OPTION_NAME and \
            last_option.group == MISC_GROUP:
        game_options.pop()


def make_target_suboptions(targets: list[Card], card_name: t.Callable[[Card], str]) -> list[GameOption]:
    return [
        GameOption(
            option=card_name(target),
            group=TARGET_GROUP,
            entity_id=target.id,
            card_type=CardType(target.type),
            zone=Zone(target.zone),
            zone_pos=target.tags.get(GameTag.ZONE_POSITION, 0),
            suboptions=[]
        )
        for target in targets
    ]


def make_suboptions(board: Board, option: Card, targets: list[Card], card_name: t.Callable[[Card], str]) -> list[GameOption]:
    target_suboptions = make_target_suboptions(targets, card_name)
    if option.zone == Zone.HAND:
        if (option.type == CardType.MINION or option.type == CardType.LOCATION):
            return [
                GameOption(
                    option=str(possible_position),
                    group=POSITION_GROUP,
                    entity_id=option.id,
                    card_type=CardType.INVALID,
                    zone=Zone.PLAY,
                    zone_pos=possible_position,
                    suboptions=target_suboptions
                )
                for possible_position in board.free_ally_positions
            ]
        if len(target_suboptions) == 0:
            return [ANYWHERE_OPTION]
    return target_suboptions


def make_deck_option(option: Card, card_name: t.Callable[[Card], str]) -> GameOption:
    return GameOption(
        option=f'(Deck) {card_name(option)}',
        group=GameOption.make_group(option.zone),
        entity_id=option.id,
        card_type=CardType(option.type),
        zone=Zone(option.zone),
        zone_pos=option.tags.get(GameTag.ZONE_POSITION, 0),
        suboptions=[DECK_OPTION]
    )
