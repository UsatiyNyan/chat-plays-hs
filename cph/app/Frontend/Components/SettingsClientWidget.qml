import QtQuick
import QtQuick.Controls

import Frontend.Styles
import Frontend.Utils
import Frontend.Bindings


Column {
    id: root

    property var voteController

    SettingsInput {
        id: urlInput

        width: parent.width
        placeholderText: 'Stream URL'
        visible: voteController.voteClientState === VoteController.VoteClientState.NotConnected
    }

    Item {
        width: parent.width
        height: Units.px(16)
        visible: voteController.voteClientState === VoteController.VoteClientState.NotConnected
    }

    PrimaryButton {
        width: parent.width
        text: 'Connect'
        visible: voteController.voteClientState === VoteController.VoteClientState.NotConnected

        onClicked: voteController.onVoteClientButtonClicked(urlInput.text)
    }

    DangerButton {
        width: parent.width
        text: 'Disconnect'
        delay: 2500
        visible: voteController.voteClientState === VoteController.VoteClientState.Connected

        onActivated: voteController.onVoteClientButtonClicked('')
    }

    Text {
        width: parent.width
        bottomPadding: Units.px(8)

        text: 'Could not connect 😔'
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        color: Colors.textError
        font.pixelSize: 20

        visible: voteController.voteClientState === VoteController.VoteClientState.Error
    }

    PrimaryButton {
        width: parent.width
        text: 'Ok'
        visible: voteController.voteClientState === VoteController.VoteClientState.Error

        onClicked: voteController.onVoteClientButtonClicked(urlInput.text)
    }
}
