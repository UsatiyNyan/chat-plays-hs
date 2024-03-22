import sys
import logging

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuickControls2 import QQuickStyle

import cph.app.resources_rc
import cph.app.app_rc
import cph.app.backend.controller

import cph.utils.logging as cph_logging


def main(argv):
    main_logger = cph_logging.make_logger('app', logging.DEBUG)

    app = QGuiApplication(argv)
    app.setOrganizationName('@UsatiyNyan')
    app.setApplicationName('Chat Plays HS')

    QQuickStyle.setStyle('Basic')

    engine = QQmlApplicationEngine()
    engine.addImportPath(':/')
    engine.loadFromModule('Frontend', 'Main.qml')

    if not engine.rootObjects():
        main_logger.error('Failed to load QML file')
        return -1

    return app.exec()


if __name__ == '__main__':
    sys.exit(main(sys.argv))
