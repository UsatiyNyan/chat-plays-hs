import pytest
import logging

from hearthstone.enums import CardType, Zone

from cph.utils.logging import make_logger
from cph.utils.vec import Vec2
from cph.game.board import WindowBB, Board, locate
from cph.game.model import GameOption


@pytest.fixture
def logger():
    return make_logger('test', logging.DEBUG)


@pytest.fixture
def window_bb():
    return WindowBB(Vec2(0, 0), Vec2(1920, 1080))


STUB_GAME_OPTION = GameOption(
    option='option',
    group='group',
    entity_id=0,
    card_type=CardType.INVALID,
    zone=Zone.INVALID,
    zone_pos=0,
    suboptions=[]
)
