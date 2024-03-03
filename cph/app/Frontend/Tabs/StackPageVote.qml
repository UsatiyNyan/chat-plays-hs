import QtQuick

import Frontend.Styles
import Frontend.Components
import Frontend.Utils

Rectangle {
    id: root

    // inherited from outer Loader:
    // required property var controller

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
        model: controller.voteModel

        delegate: VoteDelegate {
            width: listView.width
            alias: model.alias
            option: model.option
            votes: model.votes
            votesMax: controller.voteModel.votesMax
            votesSum: controller.voteModel.votesSum
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
        secondsLeft: controller.voteSecondsLeft
        secondsTotal: controller.voteSecondsTotal
        onClicked: controller.onEndVoteClicked()
    }
}
