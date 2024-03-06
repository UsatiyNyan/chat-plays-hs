import QtQuick

import Frontend.Utils
import Frontend.Styles
import Frontend.Bindings

PrimaryButton {
    id: root

    property int secondsLeft
    property int secondsTotal
    property bool inProgress
    property int state

    visible: state !== VoteController.VoteState.Finished
    text: !inProgress 
    ? 'Next vote'
    : secondsTotal > 0 
    ? `Vote ends in ${secondsLeft} s` 
    : 'End vote' 

    background: Rectangle {
        anchors {
            top: parent.top
            bottom: parent.bottom
            left: parent.left
        }
        width: parent.width * (secondsTotal === 0 ? 1 : secondsLeft / secondsTotal)
        Behavior on width { NumberAnimation { duration: 1000 } }
        color: root.backgroundColor
    }
}
