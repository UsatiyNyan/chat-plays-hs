import sys

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuickControls2 import QQuickStyle

import cph.app.resources_rc
import cph.app.app_rc


# TODO: add file watcher and reload QML on change
def main(argv):
    app = QGuiApplication(argv)
    app.setOrganizationName('@UsatiyNyan')
    app.setApplicationName('Chat Plays HS')

    QQuickStyle.setStyle('Basic')

    engine = QQmlApplicationEngine()
    engine.addImportPath(':/')
    engine.loadFromModule('Frontend', 'Main.qml')

    if not engine.rootObjects():
        return -1

    return app.exec()


if __name__ == '__main__':
    sys.exit(main(sys.argv))
