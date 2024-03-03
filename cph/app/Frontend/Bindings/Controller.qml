import QtQuick

Item {
    // --- interface ---
    property ListModel voteModel: VoteModel {}
    property bool voteEmotes: true
    property int voteSecondsLeft: 10
    property int voteSecondsTotal: 10
    property int voteWinnerIndex: -1
    property bool voteWinnerHasCandidates: true

    function onVoteButtonClicked() {
        voteWinnerIndex = voteWinnerIndex === -1 ? 5 : -1
    }

    // --- debug ---
    onVoteEmotesChanged: {
        console.log('voteEmotes', voteEmotes)
    }

    onVoteSecondsTotalChanged: {
        console.log('voteSecondsTotal', voteSecondsTotal)
    }

    Timer {
        interval: 1000
        running: voteSecondsTotal > 0
        repeat: true
        onTriggered: {
            if (voteSecondsLeft <= 0) {
                voteSecondsLeft = voteSecondsTotal
            } else {
                voteSecondsLeft -= 1
            }
        }
    }
}
