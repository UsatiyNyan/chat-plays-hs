import QtQuick

import Frontend.Bindings

PrimaryButton {
    id: root

    property int secondsLeft
    property int secondsTotal
    property int voteState

    text: getText(voteState)

    function getText(aVoteState) {
        switch (aVoteState) {
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
        width: parent.width * getRatio(root.voteState, root.secondsLeft, root.secondsTotal)
        Behavior on width { NumberAnimation { duration: 1000 } }
        color: root.backgroundColor
    }

    function getRatio(aVoteState, secondsLeft, secondsTotal) {
        if (aVoteState === VoteController.VoteState.InProgress && secondsTotal > 0) {
            return secondsLeft / secondsTotal
        }
        return 1
    }
}
