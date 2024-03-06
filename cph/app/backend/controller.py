from PySide6.QtCore import QObject, Property
from PySide6.QtQml import qmlRegisterType

from .vote.controller import VoteController
from .game.controller import GameController


class Controller(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._voteController = VoteController(self.on_vote_button_clicked)
        self._gameController = GameController()

    @Property(VoteController, constant=True)
    def voteController(self):
        return self._voteController

    @Property(GameController, constant=True)
    def gameController(self):
        return self._gameController

    def on_vote_button_clicked(self):
        pass


qmlRegisterType(Controller, 'Frontend.Bindings', 1, 0, 'Controller')
