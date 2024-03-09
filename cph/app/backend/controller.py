import logging

from PySide6.QtCore import QObject, Property
from PySide6.QtQml import qmlRegisterType

from cph.utils.logging import make_logger

from .vote.controller import VoteController
from .vote.handler import VoteHandler
from .game.controller import GameController
from .game.parser import PowerLogParser


class Controller(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._voteController = VoteController(self.on_vote_button_clicked)
        self._gameController = GameController()

        self._logger = make_logger('app', logging.DEBUG)
        self._handler = VoteHandler(self._voteController, self._logger)
        self._parser = PowerLogParser(self._handler, self._logger)

    @Property(VoteController, constant=True)
    def voteController(self):
        return self._voteController

    @Property(GameController, constant=True)
    def gameController(self):
        return self._gameController

    def on_vote_button_clicked(self):
        pass


qmlRegisterType(Controller, 'Frontend.Bindings', 1, 0, 'Controller')
