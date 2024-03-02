import QtQuick
import QtQuick.Controls

import Frontend.Styles
import Frontend.Utils

Button {
    id: root

    required property string iconName

    width: Units.px(20)
    height: Units.px(20)
    padding: 0

    checkable: false
    hoverEnabled: true
    
    icon {
        source: Resources.icon(iconName)
        color: root.down 
            ? Colors.iconSecondary
            : Colors.iconInverse
    }

    background: Rectangle {
        color: root.down 
            ? Colors.buttonSecondaryActive 
            : root.hovered
            ? Colors.buttonSecondaryHover
            : Colors.buttonSecondary
    }
}
