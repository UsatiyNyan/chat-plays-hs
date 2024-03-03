import QtQuick

import Frontend.Utils
import Frontend.Styles

Item {
    id: root

    property alias text: text.text

    height: Units.px(32) 

    Text {
        id: text
        anchors {
            top: parent.top
            left: parent.left
            right: parent.right
            bottom: parent.bottom
            topMargin: Units.px(4)
            bottomMargin: Units.px(4)
        }
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        color: Colors.textSecondary
        font.pixelSize: 20
    }
}
