import typing as t
from logging import Logger

import pyautogui

from cph.game.model import GameOption
from cph.app.backend.vote import misc

from .board import Board
from .window import WindowBB, click
from .locate import locate


def choose_button(option: str, group: str) -> t.Literal['primary', 'secondary']:
    return pyautogui.SECONDARY \
        if (group == misc.MISC_GROUP and option == misc.EMOTE_OPTION_NAME) \
        else pyautogui.PRIMARY


def interact(logger: Logger,
             window_bb: WindowBB,
             board: Board | None,
             game_options: list[GameOption],
             index: int) -> bool:
    game_option = game_options[index]
    logger.debug('[interact] begin\n'
                 f'\t{board=}\n'
                 f'\toption={game_option.option}\n'
                 f'\tgroup={game_option.group}\n'
                 f'\tid={game_option.entity_id}\n'
                 f'\tcard_type={game_option.card_type}\n'
                 f'\tzone={game_option.zone}\n'
                 f'\tzone_pos={game_option.zone_pos}\n'
                 '[interact] end')
    location = locate(logger, window_bb, board, game_options, index)
    if location is None:
        return False
    button = choose_button(game_option.option, game_option.group)
    logger.debug(f'[click] {location=} {button=}')
    return click(window_bb, location, button)
