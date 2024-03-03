import QtQuick

import Frontend.Utils
import Frontend.Styles

Item {
    id: root

    property int secondsLeft
    property int secondsTotal
    property bool inProgress
    signal clicked

    height: Units.px(35)

    Rectangle {
        anchors {
            top: parent.top
            bottom: parent.bottom
            left: parent.left
        }
        width: parent.width * (secondsTotal === 0 ? 1 : secondsLeft / secondsTotal)
        Behavior on width { NumberAnimation { duration: 1000 } }
        color: mouseArea.pressed
        ? Colors.buttonPrimaryActive
        : mouseArea.containsMouse
        ? Colors.buttonPrimaryHover
        : Colors.buttonPrimary
    }

    Text {
        anchors.fill: parent
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        color: Colors.textOnColor
        font.pixelSize: 20

        text: !inProgress 
        ? 'Next vote'
        : secondsTotal > 0 
        ? `Vote ends in ${secondsLeft} s` 
        : 'End vote' 
    }

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        hoverEnabled: true
        onClicked: root.clicked()
    }
}
