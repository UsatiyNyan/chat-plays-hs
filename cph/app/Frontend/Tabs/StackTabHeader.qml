import QtQuick
import QtQuick.Controls

import Frontend.Styles
import Frontend.Utils

Rectangle {
    id: root

    property string title

    enum State {
        OnTop,
        Selected,
        OnBottom
    }
    
    property int state
    signal clicked()

    color: Colors.background

    Rectangle {
        anchors.fill: parent
        color: mouseArea.containsMouse ? Colors.backgroundHover : 'transparent' 
    }

    Rectangle {
        anchors {
            bottom: parent.bottom
            left: parent.left
            right: parent.right
        }
        height: Units.px(1)
        color: Colors.borderSubtle01
    }

    Text {
        anchors.centerIn: parent
        text: root.title
        color: Colors.textPrimary
        font.pixelSize: 24
    }

    // use Button for icon, since Image doesn't support color field
    Button {
        anchors {
            left: root.left
            verticalCenter: root.verticalCenter
        }
        background: null
        icon {
            source: Resources.icon(_getIcon(root.state))
            color: Colors.iconPrimary
        }

        function _getIcon(_state) {
            switch (_state) {
                case StackTabHeader.State.OnTop: return 'chevron-down'
                case StackTabHeader.State.OnBottom: return 'chevron-up'
                case StackTabHeader.State.Selected: return 'subtract-large'
            }
        }
    }

    MouseArea {
        id: mouseArea

        anchors.fill: parent
        onClicked: root.clicked()
        hoverEnabled: true
    }
}
