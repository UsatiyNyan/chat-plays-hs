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

    Loader {
        id: content

        anchors {
            top: header.bottom
            left: parent.left
            right: parent.right
        }
        Behavior on height {
            PropertyAnimation {
                duration: 200
                easing.type: Easing.InOutQuad
            }
        }
        active: height > 0
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

