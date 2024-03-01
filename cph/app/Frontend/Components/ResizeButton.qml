import QtQuick

WindowControlButton {
    id: root

    required property var target
    required property int edge

    iconName: 'resize'  // right-left default rotation

    transform: Rotation {
        origin { x: width / 2; y: height / 2 }
        angle: edge & Qt.LeftEdge ? 90 : 0
    }

    onPressed: target.startSystemResize(edge)
}
