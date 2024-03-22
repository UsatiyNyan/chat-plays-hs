from logging import Logger
from hearthstone.enums import CardType, Zone

from cph.utils.vec import Vec2
from cph.game.model import GameOption
from cph.app.backend.vote import misc

from .board import Board
from .window import WindowBB

center = Vec2(960, 500)
enemy_y = 410
ally_y = 590
minion_offset_x = 140


def locate_choice(logger: Logger, window_bb: WindowBB, size: int, index: int) -> Vec2 | None:
    logger.debug(f'[locate] choice {size=} {index=}')
    match size:
        case 1:
            return center
        case 2:
            begin_x = center.x - 120
            return Vec2(begin_x + index * 240, center.y)
        case 3:
            begin_x = center.x - 400
            return Vec2(begin_x + index * 400, center.y)
        case 4:
            begin_x = center.x - 360
            return Vec2(begin_x + index * 240, center.y)
    return None


hand_positions = {
    1: [Vec2(880, 960)],
    2: [Vec2(815, 960), Vec2(945, 960)],
    3: [Vec2(750, 960), Vec2(885, 960), Vec2(1020, 960)],
    4: [Vec2(670, 1000), Vec2(815, 970), Vec2(950, 970), Vec2(1100, 990)],
    5: [Vec2(655, 1000), Vec2(780, 980), Vec2(890, 970), Vec2(1000, 970), Vec2(1115, 990)],  # noqa
    6: [Vec2(650, 1010), Vec2(750, 980), Vec2(840, 970), Vec2(930, 970), Vec2(1030, 970), Vec2(1120, 990)],  # noqa
    7: [Vec2(640, 1015), Vec2(720, 990), Vec2(800, 980), Vec2(880, 970), Vec2(960, 970), Vec2(1050, 980), Vec2(1135, 990)],  # noqa
    8: [Vec2(640, 1020), Vec2(710, 1000), Vec2(780, 980), Vec2(850, 970), Vec2(920, 970), Vec2(990, 970), Vec2(1060, 980), Vec2(1140, 995)],  # noqa
    9: [Vec2(640, 1020), Vec2(700, 1005), Vec2(760, 990), Vec2(820, 980), Vec2(880, 970), Vec2(945, 970), Vec2(1015, 975), Vec2(1080, 980), Vec2(1145, 1000)],  # noqa
    10: [Vec2(630, 1030), Vec2(690, 1010), Vec2(740, 995), Vec2(800, 985), Vec2(860, 975), Vec2(920, 970), Vec2(980, 970), Vec2(1030, 975), Vec2(1090, 985), Vec2(1150, 1000)],  # noqa
    11: [Vec2(630, 1030), Vec2(680, 1020), Vec2(730, 1005), Vec2(780, 995), Vec2(830, 985), Vec2(880, 975), Vec2(930, 970), Vec2(980, 970), Vec2(1030, 975), Vec2(1090, 985), Vec2(1150, 1000)],  # noqa
}


def locate_hand(logger: Logger, window_bb: WindowBB, board: Board, zone_pos: int) -> Vec2 | None:
    logger.debug('[locate] hand')
    hand_size = len(board.hand)
    if zone_pos < 1 or zone_pos > hand_size:
        logger.error(f'[locate] invalid {zone_pos=}')
        return None

    current_hand = hand_positions.get(hand_size)
    if current_hand is None:
        logger.error(f'[locate] invalid {hand_size=}')
        return None

    zone_pos_normalized = zone_pos - 1
    assert zone_pos_normalized < len(current_hand)
    return current_hand[zone_pos_normalized]


def locate_minion(logger: Logger, window_bb: WindowBB,
                  board: Board, zone_pos: int, is_ally: bool) -> Vec2 | None:
    logger.debug(f'[locate] minion {is_ally=}')
    if zone_pos < 1 or zone_pos > 7:
        logger.error(f'[locate] invalid zone_pos {zone_pos=}')
        return None
    y = ally_y if is_ally else enemy_y
    minions = board.ally_minions if is_ally else board.enemy_minions
    if len(minions) == 0:
        logger.error('[locate] no minions')
        return None
    minions_width = minion_offset_x * (len(minions) - 1)
    begin_x = center.x - minions_width // 2
    x = begin_x + minion_offset_x * (zone_pos - 1)
    return Vec2(x, y)


def locate_ally_placement(logger: Logger, window_bb: WindowBB,
                          board: Board, index: int) -> Vec2:
    logger.debug(f'[locate] position {index=}')
    minions = board.ally_minions
    minions_width = minion_offset_x * len(minions)
    begin_x = center.x - minions_width // 2
    x = begin_x + minion_offset_x * index
    return Vec2(x, ally_y)


def locate_hero(logger: Logger, window_bb: WindowBB, is_ally: bool) -> Vec2:
    logger.debug(f'[locate] hero {is_ally=}')
    y = 800 if is_ally else 200
    return Vec2(center.x, y)


def locate_hero_power(logger: Logger, window_bb: WindowBB) -> Vec2:
    logger.debug('[locate] hero power')
    return Vec2(1140, 830)


def locate_end_turn(logger: Logger, window_bb: WindowBB) -> Vec2:
    logger.debug('[locate] end turn')
    return Vec2(1550, center.y)


def locate_anywhere(logger: Logger, window_bb: WindowBB) -> Vec2:
    logger.debug('[locate] anywhere')
    return center


emote_positions = (
    Vec2(770, 860),
    Vec2(760, 770),
    Vec2(800, 680),
    Vec2(1120, 680),
    Vec2(1160, 770),
    Vec2(1150, 860),
)


def locate_emote(logger: Logger, window_bb: WindowBB, index: int) -> Vec2 | None:
    logger.debug(f'[locate] emote {index=}')
    if index < 0 or index >= len(emote_positions):
        return None
    return emote_positions[index]


def locate(logger: Logger,
           window_bb: WindowBB,
           board: Board | None,
           game_options: list[GameOption],
           index: int) -> Vec2 | None:
    if board is None:
        return locate_choice(logger, window_bb, len(game_options), index)

    game_option = game_options[index]

    is_hand = game_option.zone == Zone.HAND
    if is_hand:
        return locate_hand(logger, window_bb, board, game_option.zone_pos)

    is_position = game_option.group == misc.POSITION_GROUP
    if is_position:
        if game_option.option == misc.ANYWHERE_OPTION_NAME:
            return locate_anywhere(logger, window_bb)

        return locate_ally_placement(logger, window_bb, board, index)

    is_hero = game_option.card_type == CardType.HERO
    if is_hero:
        is_ally = board.ally_hero == game_option.entity_id
        return locate_hero(logger, window_bb, is_ally)

    is_hero_power = game_option.card_type == CardType.HERO_POWER
    if is_hero_power:
        return locate_hero_power(logger, window_bb)

    is_play = game_option.zone == Zone.PLAY
    if is_play:
        is_ally = game_option.entity_id in board.ally_minions
        return locate_minion(logger, window_bb, board, game_option.zone_pos, is_ally)

    is_misc = game_option.group == misc.MISC_GROUP
    if is_misc:
        if game_option.option == misc.EMOTE_OPTION_NAME:
            return locate_hero(logger, window_bb, is_ally=True)

        if game_option.option == misc.END_TURN_OPTION_NAME:
            return locate_end_turn(logger, window_bb)

        if game_option.option in misc.EMOTE_SUBOPTIONS:
            return locate_emote(logger, window_bb, index)

        logger.error(f'[locate] misc missed {game_option}')
        return None

    # TODO: DECK: FORGE, TRADE
    logger.error(f'[locate] missed {game_option}')
    return None
