import QtQuick
import QtQuick.Controls

import Frontend.Colors
import Frontend.Components
import Frontend.Utils

ApplicationWindow {
    id: root
    width: Units.px(400)
    height: Units.px(800)
    visible: true
    flags: Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint
    color: Colors.background

    WindowDragHandler {
        dragWindow: root
        anchors.fill: parent
    }

    ResizeButton {
        anchors { left: parent.left; bottom: parent.bottom }
        target: root
        edge: Qt.BottomEdge | Qt.LeftEdge
    }
}
