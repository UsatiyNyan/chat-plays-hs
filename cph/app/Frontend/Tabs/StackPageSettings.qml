import QtQuick

import Frontend.Styles
import Frontend.Components
import Frontend.Utils

Rectangle {
    id: root

    // inherited from outer Loader:
    // required property var controller
    readonly property var voteController: controller.voteController
    readonly property var gameController: controller.gameController

    clip: true
    color: Colors.background

    Column {
        anchors.fill: parent
        spacing: Units.px(16)
        topPadding: Units.px(16)

        SettingsSwitch {
            id: voteEmotesSwitch

            width: parent.width
            text: 'Vote for Emotes'

            Component.onCompleted: checked = voteController.voteEmotes
            onCheckedChanged: voteController.voteEmotes = checked
        }

        Rectangle {
            width: parent.width
            height: Units.px(1)
            color: Colors.borderSubtle01
        }

        SettingsSlider {
            id: voteSecondsSlider

            width: parent.width

            text: 'Total vote time is ' + (value === 0 ? '♾ ': `${value}s`)
            from: 0
            to: 40
            stepSize: 1

            Component.onCompleted: value = voteController.voteSecondsTotal
            onValueChanged: voteController.voteSecondsTotal = value
        }

        Rectangle {
            width: parent.width
            height: Units.px(1)
            color: Colors.borderSubtle01
        }

        SettingsClientWidget {
            width: parent.width

            voteController: root.voteController
        }

        Rectangle {
            width: parent.width
            height: Units.px(1)
            color: Colors.borderSubtle01
        }

        PrimaryButton {
            id: enablePowerLogButton

            enabled: !gameController.isPowerLogEnabled
            width: parent.width

            text: enabled ? 'Enable Power Log' : 'Power Log is enabled'
            onClicked: gameController.enablePowerLog()
        }
    }
}
