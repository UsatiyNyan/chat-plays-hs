from PySide6.QtCore import QObject, Property
from PySide6.QtQml import qmlRegisterType

from .vote.controller import VoteController


class Controller(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._vote_controller = VoteController(self.on_vote_button_clicked)

    @Property(VoteController, constant=True)
    def voteController(self):
        return self._vote_controller

    def on_vote_button_clicked(self):
        pass


qmlRegisterType(Controller, 'Frontend.Bindings', 1, 0, 'Controller')
