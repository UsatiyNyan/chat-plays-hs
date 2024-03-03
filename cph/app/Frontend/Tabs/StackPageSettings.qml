import QtQuick

import Frontend.Styles
import Frontend.Components
import Frontend.Utils

Rectangle {
    id: root

    // inherited from outer Loader:
    // required property var controller

    clip: true
    color: Colors.background

    Column {
        anchors.fill: parent
        spacing: Units.px(4)

        SettingsSwitch {
            id: voteEmotesSwitch

            width: parent.width

            text: 'Vote for Emotes'
            checked: { checked = controller.voteEmotes }
            onCheckedChanged: { controller.voteEmotes = checked }
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

            value: { value = controller.voteSecondsTotal }
            onValueChanged: { controller.voteSecondsTotal = value }
        }
    }
}
