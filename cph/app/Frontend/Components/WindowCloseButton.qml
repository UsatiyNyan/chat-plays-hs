import QtQuick

WindowControlButton {
    id: root

    required property var target

    iconName: 'close'
    onPressed: target.close()
}
