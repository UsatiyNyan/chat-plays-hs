import QtQuick

import Frontend.Styles
import Frontend.Components
import Frontend.Utils

Rectangle {
    id: root

    // inherited from outer Loader:
    // required property var controller

    color: Colors.layer01
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
            text: model.alias
        }
        
        section {
            property: "header"
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
