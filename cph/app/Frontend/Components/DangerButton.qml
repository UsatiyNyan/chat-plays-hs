import QtQuick
import QtQuick.Controls

import Frontend.Utils
import Frontend.Styles

DelayButton {
    id: root

    height: Units.px(36)
    hoverEnabled: true
    font.pixelSize: 20
    readonly property color backgroundColor: root.pressed
    ? Colors.buttonDangerActive
    : root.hovered
    ? Colors.buttonDangerHover
    : Colors.buttonDangerPrimary

    background: Rectangle {
        color: root.backgroundColor
        width: parent.width * (1 - root.progress)
    }

    contentItem: Text {
        text: root.text
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        color: Colors.textOnColor
        font: root.font
    }
}

