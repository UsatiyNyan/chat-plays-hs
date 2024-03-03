import QtQuick
import QtQuick.Controls

import Frontend.Styles
import Frontend.Utils

Item {
    id: root

    property alias text: label.text
    property alias checked: switchControl.checked
    
    height: Units.px(24)

    Text {
        id: label
        anchors {
            left: parent.left
            leftMargin: Units.px(16)
            verticalCenter: parent.verticalCenter
        }
        color: Colors.textSecondary
        font.pixelSize: 20
    }

    Switch {
        id: switchControl

        anchors.right: parent.right
        height: Units.px(24)

        indicator: Rectangle {
            implicitWidth: Units.px(48)
            implicitHeight: radius * 2
            x: parent.leftPadding
            y: parent.height / 2 - height / 2
            radius: Units.px(12)
            color: switchControl.checked ? Colors.supportSuccess : Colors.toggleOff

            Rectangle {
                x: switchControl.checked 
                ? parent.width - parent.radius - radius 
                : parent.radius - radius
                y: parent.height / 2 - height / 2
                width: radius * 2
                height: radius * 2
                radius: Units.px(9)
                color: Colors.iconOnColor

                Behavior on x { NumberAnimation { duration: 100 } }
            }
        }
    }
}
