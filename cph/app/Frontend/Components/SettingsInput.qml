import QtQuick
import QtQuick.Controls

import Frontend.Styles
import Frontend.Utils
import Frontend.Bindings

TextField {
    id: root

    placeholderTextColor: Colors.textPlaceholder
    wrapMode: TextInput.WrapAnywhere
    height: contentHeight + topPadding + bottomPadding
    font.pixelSize: 16
    color: Colors.textPrimary

    background: Rectangle {
        color: Colors.layer01
        border {
            color: Colors.borderTile01
            width: Units.px(1)
        }
    }
}

