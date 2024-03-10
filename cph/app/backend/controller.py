import logging

from PySide6.QtCore import QObject, Property, QTimer
from PySide6.QtQml import qmlRegisterType

from cph.utils.logging import make_logger
from cph.vote.machine import VoteMachine

from .vote.controller import VoteController
from .vote.handler import VoteHandler
from .game.controller import GameController
from .game.parser import PowerLogParser


class Controller(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._voteController = VoteController()
        self._gameController = GameController()

        self._logger = make_logger('app', logging.DEBUG)
        self._machine = VoteMachine(self._logger)
        self._handler = VoteHandler(self._voteController, self._machine, self._logger)
        self._parser = PowerLogParser(self._handler, self._logger)

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


qmlRegisterType(Controller, 'Frontend.Bindings', 1, 0, 'Controller')
