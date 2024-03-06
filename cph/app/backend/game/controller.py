from PySide6.QtCore import QObject, Property, Signal, Slot
from PySide6.QtQml import qmlRegisterType

from cph.game import log_config


class GameController(QObject):
    isPowerLogEnabledChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._isPowerLogEnabled = log_config.power_is_enabled()

    @Property(bool, notify=isPowerLogEnabledChanged)
    def isPowerLogEnabled(self):
        return self._isPowerLogEnabled

    @isPowerLogEnabled.setter
    def isPowerLogEnabled(self, value):
        if self._isPowerLogEnabled != value:
            self._isPowerLogEnabled = value
            self.isPowerLogEnabledChanged.emit()

    @Slot()
    def enablePowerLog(self):
        if self.isPowerLogEnabled:
            return
        self.isPowerLogEnabled = log_config.power_enable()


qmlRegisterType(GameController, 'Frontend.Bindings', 1, 0, 'GameController')
