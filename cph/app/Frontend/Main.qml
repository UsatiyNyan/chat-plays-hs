import QtQuick
import QtQuick.Controls

import Frontend.Styles
import Frontend.Components
import Frontend.Utils
import Frontend.Tabs

ApplicationWindow {
    id: root
    width: Units.px(400)
    height: Units.px(800)
    visible: true
    flags: Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint
    color: Colors.background

    WindowDragArea {
        dragWindow: root
        anchors.fill: parent
    }

    StackTabView {
        anchors { fill: parent; margins: Units.px(10) }
        controller: QtObject {
            property ListModel voteModel: ListModel {
                ListElement { name: "Vote 1" }
                ListElement { name: "Vote 2" }
                ListElement { name: "Vote 3" }
                ListElement { name: "Vote 4" }
            }
        }
    }

    CloseButton {
        anchors { right: parent.right; top: parent.top }
        target: root
    }

    ResizeButton {
        anchors { left: parent.left; bottom: parent.bottom }
        target: root
        edge: Qt.BottomEdge | Qt.LeftEdge
    }
}
