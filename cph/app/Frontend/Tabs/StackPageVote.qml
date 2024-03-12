import QtQuick

import Frontend.Styles
import Frontend.Components
import Frontend.Utils

Rectangle {
    id: root

    // inherited from outer Loader:
    // required property var controller
    readonly property var voteController: controller.voteController

    color: Colors.background
    clip: true

    ListView {
        id: listView

        anchors {
            top: parent.top
            left: parent.left
            right: parent.right
        }
        height: parent.height - button.height
        interactive: false
        model: voteController.voteModel
        currentIndex: -1

        delegate: VoteDelegate {
            width: listView.width
            alias: model.alias
            option: model.option
            votes: model.votes
            votesMax: voteController.voteModel.votesMax
            votesSum: voteController.voteModel.votesSum
            winnerIndices: voteController.voteWinnerIndices
        }
        
        section {
            property: 'group'
            criteria: ViewSection.FullString
            delegate: VoteHeader {
                width: listView.width
                text: section
            }
        }
    }

    VoteButton {
        id: button
        anchors {
            top: listView.bottom
            left: parent.left
            right: parent.right
        }
        secondsLeft: voteController.voteSecondsLeft
        secondsTotal: voteController.voteSecondsTotal
        onClicked: voteController.onVoteButtonClicked()
        state: voteController.voteState
    }
}
