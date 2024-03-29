import QtQuick

import Frontend.Utils
import Frontend.Styles
import Frontend.Bindings

Item {
    id: root

    property string alias
    property string option
    property int votes
    property int votesMax
    property int votesSum
    property var winnerIndices
    property int voteState

    height: Units.px(30)

    Rectangle {
        id: background
        anchors {
            fill: parent
            leftMargin: Units.px(8)
            rightMargin: Units.px(8)
        }
        color: Colors.background
    }

    Rectangle {
        anchors {
            top: background.top
            bottom: background.bottom
            left: background.left
        }
        width: MathExt.safeFraction(votes, votesMax, 0) * background.width
        color: root.voteState === VoteController.VoteState.InProgress || 
        (root.winnerIndices.indexOf(index) !== -1 && root.voteState === VoteController.VoteState.Finished)
        ? Colors.tagBackgroundGreen : 'transparent'
        Behavior on width { NumberAnimation { duration: 500 } }
    }

    Rectangle {
        anchors.fill: background
        border {
            width: Units.px(1)
            color: Colors.borderSubtle01
        }
        color: 'transparent'
    }

    Text {
        anchors {
            verticalCenter: background.verticalCenter
            left: background.left
            leftMargin: Units.px(8)
            right: fractionText.left
        }
        text: `${alias}: ${option}`
        color: Colors.textOnColor
        font.pixelSize: 20
    }

    Text {
        id: fractionText
        anchors {
            verticalCenter: background.verticalCenter
            right: background.right
            rightMargin: Units.px(8)
        }
        text: (MathExt.safeFraction(votes, votesSum, 0) * 100.0).toFixed(1) + '%'
        color: Colors.textOnColor
        font.pixelSize: 20
    }
}

