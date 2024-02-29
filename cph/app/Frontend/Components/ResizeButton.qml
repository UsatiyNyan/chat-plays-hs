import QtQuick
import QtQuick.Controls

import Frontend.Colors
import Frontend.Utils

Button {
    id: root

    property var target
    property int edge

    width: Units.px(20)
    height: Units.px(20)

    checkable: false
    hoverEnabled: true

    background: Rectangle {
        color: root.down 
            ? Colors.buttonPrimaryActive 
            : root.hovered
            ? Colors.buttonPrimaryHover
            : Colors.buttonPrimary
    }

    onPressed: {
        target.startSystemResize(edge)
    }
}
