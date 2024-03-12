import QtQuick

Item {
    // --- interface ---
    enum VoteState {
        Ready,
        InProgress,
        Finished
    }

    readonly property ListModel voteModel: VoteModel {}
    property bool voteEmotes: true
    property int voteSecondsLeft: 10
    property int voteSecondsTotal: 10
    property list<int> voteWinnerIndices: []
    property int voteState: VoteController.VoteState.InProgress

    function onVoteButtonClicked() {
        voteState = _nextVoteState()
    }

    function _nextVoteState() {
        switch (voteState) {
            case VoteController.VoteState.Ready:
                return VoteController.VoteState.InProgress
            case VoteController.VoteState.InProgress:
                return VoteController.VoteState.Finished
            case VoteController.VoteState.Finished:
                return VoteController.VoteState.Ready
        }
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
