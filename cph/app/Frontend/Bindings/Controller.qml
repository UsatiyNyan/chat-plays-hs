import QtQuick

Item {
    property ListModel voteModel: VoteModel {}
    property int voteSecondsLeft: 10
    property int voteSecondsTotal: 10

    function onEndVoteClicked() {
        console.log("End vote clicked")
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
