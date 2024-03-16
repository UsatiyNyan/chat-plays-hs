import logging

from PySide6.QtCore import QObject, Property, QTimer, Slot
from PySide6.QtQml import qmlRegisterType

from cph.utils.logging import make_logger

from .vote.controller import VoteController
from .vote.handler import VoteHandler
from .game.controller import GameController
from .game.parser import PowerLogParser


class Controller(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        app_logger = make_logger('app', logging.DEBUG)
        self._voteController = VoteController(app_logger)
        self._gameController = GameController()

        self._handler = VoteHandler(self._voteController, app_logger)
        parser_logger = app_logger.getChild('parser')
        parser_logger.setLevel(logging.WARNING)
        self._parser = PowerLogParser(self._handler, parser_logger)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.setSingleShot(False)
        self._timer.start(1000)

    @Property(VoteController, constant=True)
    def voteController(self):
        return self._voteController

    @Property(GameController, constant=True)
    def gameController(self):
        return self._gameController

    def _tick(self):
        self._parser.parse_once()
        self._voteController.tick()

    @Slot()
    def close(self):
        self._timer.stop()
        self._voteController.close()


qmlRegisterType(Controller, 'Frontend.Bindings', 1, 0, 'Controller')
