import QtQuick

import Frontend.Utils
import Frontend.Styles

Item {
    id: root

    property string text
    property int voteCount

    height: Units.px(30)

    Text {
        text: root.text
    }
}

