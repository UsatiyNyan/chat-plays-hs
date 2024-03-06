import QtQuick
import QtQuick.Controls

import Frontend.Utils
import Frontend.Styles
import Frontend.Bindings

Button {
    id: root

    height: Units.px(36)
    hoverEnabled: true
    font.pixelSize: 20
    readonly property color backgroundColor: root.pressed
    ? Colors.buttonPrimaryActive
    : root.hovered
    ? Colors.buttonPrimaryHover
    : Colors.buttonPrimary

    background: Rectangle {
        color: root.backgroundColor
    }

    contentItem: Text {
        text: root.text
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        color: Colors.textOnColor
        font: root.font
    }
}

