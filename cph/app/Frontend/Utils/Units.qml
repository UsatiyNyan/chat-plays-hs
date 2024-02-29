pragma Singleton
import QtQuick

QtObject {
    readonly property real aspectRatio: 16 / 9  // width / height

    function px(value) { return value / Screen.devicePixelRatio }
    function xp(value) { return value * Screen.devicePixelRatio }

    function aspectWidth(height) { return aspectRatio * height }
    function aspectHeight(width) { return width / aspectRatio }
}
