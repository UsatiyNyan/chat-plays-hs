import QtQuick
import QtQuick.Controls
import Frontend
import Frontend.Colors

ApplicationWindow {
    id: root
    width: 1100
    height: 600
    visible: true
    flags: Qt.Window | Qt.WindowStaysOnTopHint | Qt.WA_TranslucentBackground | Qt.FramelessWindowHint
    color: "transparent"

    Rectangle {
        id: background
        width: root.width
        height: root.height
        color: Colors.background
        opacity: 0.8
    }
}
