import sys

from PySide6.QtCore import QDir

import cph.app.resources_rc
import cph.app.app_rc


def walk_dir(qdir: QDir):
    for entry in qdir.entryList():
        print(qdir.absoluteFilePath(entry))
        if qdir.cd(entry):
            walk_dir(qdir)
            qdir.cdUp()


def main():
    walk_dir(QDir(':/'))


if __name__ == '__main__':
    sys.exit(main())

