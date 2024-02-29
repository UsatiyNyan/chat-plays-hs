import QtQuick
import QtQuick.Controls

import Frontend
import Frontend.Colors
import Frontend.Components

ApplicationWindow {
    id: root
    width: 1100
    height: 600
    visible: true
    flags: Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint

    Rectangle {
        id: background
        width: root.width
        height: root.height
        color: Colors.background
    }

    ResizeButton {
        anchors {
            left: parent.left
            bottom: parent.bottom
        }
        target: root
        edge: Qt.BottomEdge | Qt.LeftEdge
    }
}
