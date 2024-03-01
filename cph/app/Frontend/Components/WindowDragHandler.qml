import QtQuick
import QtQuick.Controls

Item {
    required property ApplicationWindow dragWindow
    
    DragHandler {
        target: null
        cursorShape: Qt.ClosedHandCursor

        onActiveChanged: {
            if (active) dragWindow.startSystemMove()
        }
    }

    HoverHandler {
        cursorShape: Qt.OpenHandCursor
    }
}
