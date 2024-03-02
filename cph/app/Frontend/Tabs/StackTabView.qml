import QtQuick
import QtQuick.Controls

import Frontend.Styles
import Frontend.Utils

Rectangle {
    id: root        

    readonly property int headerHeight: Units.px(40)
    readonly property int contentHeight: height - (headerHeight * listView.model.count) 

    color: Colors.backgroundActive

    ListView {
        id: listView

        height: headerHeight * model.count + contentHeight
        anchors {
            top: parent.top
            left: parent.left
            right: parent.right
        }
        currentIndex: -1

        model: ListModel {
            ListElement {
                title: "settings"
                // content: TabSettings {}
            }
            ListElement {
                title: "vote"
                // content: TabVote {}
            }
            ListElement {
                title: "connect"
                // content: TabConnect {}
            }
        }

        delegate: StackTabDelegate {
            width: listView.width
            headerHeight: root.headerHeight
            contentHeight: listView.currentIndex === index ? root.contentHeight : 0 

            title: model.title
            // content: model.content

            onTitleClicked: listView.currentIndex = listView.currentIndex === index ? -1 : index
        }
    }
}
