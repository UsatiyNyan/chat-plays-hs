from PySide6.QtCore import QObject, Property
from PySide6.QtQml import qmlRegisterType

from cph.app.backend.options.controller import DisplayOptionsController


class Controller(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._vote_controller = DisplayOptionsController()

    @Property(DisplayOptionsController, constant=True)
    def voteController(self):
        return self._vote_controller


qmlRegisterType(Controller, 'Frontend.Bindings', 1, 0, 'Controller')
