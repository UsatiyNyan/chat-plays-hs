import QtQuick

import Frontend.Styles
import Frontend.Utils

Item {
    id: root

    property alias content: content
    property alias header: header

    height: header.height + content.height

    StackTabHeader {
        id: header

        anchors {
            top: parent.top
            left: parent.left
            right: parent.right
        }
    }

    Rectangle {
        id: content

        anchors {
            top: header.bottom
            left: parent.left
            right: parent.right
        }
        color: Colors.layer01

        Behavior on height {
            PropertyAnimation {
                duration: 200
                easing.type: Easing.InOutQuad
            }
        }
    }

    Rectangle {
        anchors {
            bottom: parent.bottom
            left: parent.left
            right: parent.right
        }
        height: Units.px(1)
        color: Colors.borderSubtle01
    }
}

