import sys
from PySide6.QtWidgets import QApplication, QLabel, QWidget
from PySide6.QtCore import Qt, QTimer

import pyautogui


class AlwaysOnTopWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.timer = QTimer(self)
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.onUpdate)
        self.timer.start(100)

    def initUI(self):
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
        self.label = QLabel('', self)
        self.label.setStyleSheet("padding: 8px;")
        self.label.adjustSize()
        self.adjustSize()
        self.show()

    def onUpdate(self):
        x, y = pyautogui.position()
        self.label.setText(f'x={x} y={y}')
        self.label.adjustSize()
        self.adjustSize()


def main(argv):
    app = QApplication(argv)
    window = AlwaysOnTopWindow()
    return app.exec()


if __name__ == '__main__':
    sys.exit(main(sys.argv))
