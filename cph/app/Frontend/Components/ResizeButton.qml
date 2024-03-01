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
    padding: 0

    checkable: false
    hoverEnabled: true
    
    transform: Rotation {
        origin.x: width / 2
        origin.y: height / 2
        angle: edge & Qt.LeftEdge ? 90 : 0
    }

    icon {
        source: Resources.icon('resize')
        color: root.down 
            ? Colors.iconPrimary
            : Colors.iconInverse
    }

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
