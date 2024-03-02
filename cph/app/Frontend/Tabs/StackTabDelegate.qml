import QtQuick

import Frontend.Colors

Item {
    id: root

    property int headerHeight
    property int contentHeight
    property string title
    property var content
    signal titleClicked()

    height: headerHeight + contentHeight

    Rectangle {
        id: header

        height: root.headerHeight
        anchors {
            top: parent.top
            left: parent.left
            right: parent.right
        }
        color: Colors.buttonPrimary

        Text {
            anchors.centerIn: parent
            text: root.title
        }

        MouseArea {
            anchors.fill: parent
            onClicked: root.titleClicked()
        }
    }

    Rectangle {
        id: content

        height: root.contentHeight
        anchors {
            top: header.bottom
            left: parent.left
            right: parent.right
        }
        color: Colors.buttonSecondary
    }
}

