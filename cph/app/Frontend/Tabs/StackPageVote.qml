import QtQuick

import Frontend.Styles
import Frontend.Components
import Frontend.Utils

Rectangle {
    id: root

    // property controller inherited from Loader

    color: Colors.layer01

    ListView {
        id: listView
        model: controller.voteModel
        anchors.fill: parent
        delegate: Text {
            text: model.name
        }
    }
}
