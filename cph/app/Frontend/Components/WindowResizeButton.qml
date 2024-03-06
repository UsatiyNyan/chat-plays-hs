import QtQuick

WindowControlButton {
    id: root

    required property var target
    required property int edge

    iconName: 'maximize' 
    onPressed: target.startSystemResize(edge)
}
