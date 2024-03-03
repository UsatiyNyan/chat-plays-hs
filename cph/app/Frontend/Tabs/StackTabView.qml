import QtQuick
import QtQuick.Controls

import Frontend.Styles
import Frontend.Utils

Item {
    id: root        

    readonly property int headerHeight: Units.px(40)
    readonly property int contentHeight: height - (headerHeight * listView.model.count) 
    readonly property bool isExpanded: listView.currentIndex !== -1

    StackPagePlaceholder {
        anchors {
            left: parent.left
            right: parent.right
            bottom: parent.bottom
        }
        height: contentHeight
    }

    ListView {
        id: listView

        height: headerHeight * model.count + (isExpanded ? contentHeight : 0)
        anchors {
            top: parent.top
            left: parent.left
            right: parent.right
        }
        currentIndex: -1
        interactive: false
        model: ListModel {
            ListElement {
                title: "settings"
                content: "qrc:/Frontend/Tabs/StackPageSettings.qml"
            }
            ListElement {
                title: "vote"
                content: "qrc:/Frontend/Tabs/StackPageVote.qml"
            }
        }

        delegate: StackTabDelegate {
            width: listView.width
            content {
                height: listView.currentIndex === index ? root.contentHeight : 0
                source: model.content 
            }
            header {
                height: root.headerHeight
                title: model.title
                state: _getTabHeaderState(listView.currentIndex, index)
                onClicked: listView.currentIndex = (listView.currentIndex === index ? -1 : index)
            }
            function _getTabHeaderState(_currentIndex, _index) {
                if (_currentIndex === -1 || _currentIndex > _index) {
                    return StackTabHeader.State.OnTop
                } else if (_currentIndex < _index) {
                    return StackTabHeader.State.OnBottom
                }
                return StackTabHeader.State.Selected
            }
        }
    }
}
