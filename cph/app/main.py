import sys
import logging
from pathlib import Path

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuickControls2 import QQuickStyle

import cph.utils.logging as cph_logging


def main(argv):
    main_logger = cph_logging.make_logger('main', logging.ERROR)

    app = QGuiApplication(argv)
    app.setOrganizationName("@UsatiyNyan")
    app.setApplicationName("Chat Plays HS")

    QQuickStyle.setStyle("Basic")
    engine = QQmlApplicationEngine()

    curr_dir = Path(__file__).parent.resolve()
    engine.addImportPath(curr_dir)
    engine.loadFromModule("Frontend", "Main")

    if not engine.rootObjects():
        main_logger.error('Failed to load QML file')
        return -1

    return app.exec()


if __name__ == '__main__':
    sys.exit(main(sys.argv))
