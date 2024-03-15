import QtQuick

Item {
    // --- interface ---
    enum VoteState {
        Ready,
        InProgress,
        Finished
    }

    enum VoteClientState {
        NotConnected,
        Connected,
        Error
    }

    readonly property ListModel voteModel: VoteModel {}
    property bool voteEmotes: true
    property int voteSecondsLeft: 10
    property int voteSecondsTotal: 10
    property list<int> voteWinnerIndices: [5]
    property int voteState: VoteController.VoteState.InProgress
    property int voteClientState: VoteController.VoteClientState.NotConnected

    function onVoteButtonClicked() {
        voteState = _nextVoteState()
    }

    function onVoteClientButtonClicked(url) {
        console.log('voteClientButtonClicked', url)
        voteClientState = _nextVoteClientState()
    }

    // --- debug ---
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

    function _nextVoteClientState() {
        switch (voteClientState) {
            case VoteController.VoteClientState.NotConnected:
                return VoteController.VoteClientState.Connected
            case VoteController.VoteClientState.Connected:
                return VoteController.VoteClientState.Error
            case VoteController.VoteClientState.Error:
                return VoteController.VoteClientState.NotConnected
        }
    }

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
