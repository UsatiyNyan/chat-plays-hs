import QtQuick
import QtQuick.Controls

DragHandler {
    required property ApplicationWindow dragWindow

    target: null
    cursorShape: Qt.ClosedHandCursor

    onActiveChanged: {
        if (active) dragWindow.startSystemMove()
    }
}
