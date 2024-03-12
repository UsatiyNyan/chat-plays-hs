import QtQuick

import Frontend.Utils
import Frontend.Styles
import Frontend.Bindings

PrimaryButton {
    id: root

    property int secondsLeft
    property int secondsTotal
    property int state

    visible: state !== VoteController.VoteState.Finished
    text: getText(state)

    function getText(state) {
        switch (state) {
            case VoteController.VoteState.Ready: return 'Start vote'
            case VoteController.VoteState.InProgress: 
                return (secondsTotal > 0 ? `Vote ends in ${secondsLeft}s` : 'End vote')
            case VoteController.VoteState.Finished: return 'Next vote'
        }
    }

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
