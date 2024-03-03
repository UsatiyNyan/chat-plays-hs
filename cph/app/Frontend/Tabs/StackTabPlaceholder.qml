import QtQuick

import Frontend.Styles

Rectangle {
    id: root

    color: Colors.layer02

    Text {
        clip: true
        anchors.fill: parent
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        color: Colors.textSecondary
        font.pixelSize: 20
        wrapMode: Text.WordWrap
        text:
`To vote type: "!vote <options>"
e.g.: "!vote H2 P2 E1"

You can only vote for up to 3 candidates!
The lesser you choose the heftier the vote!

Command is case insensitive, but be careful with spaces!

Have Fun!`
    }

    Text {
        clip: true
        anchors {
            bottom: parent.bottom
            horizontalCenter: parent.horizontalCenter
        }
        color: Colors.textSecondary
        font.pixelSize: 16
        text: "made by @usatiynyan"
    }
}
