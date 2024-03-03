import QtQuick
import QtQuick.Controls

import Frontend.Styles
import Frontend.Utils

Column {
    id: root

    property alias text: label.text
    property alias value: slider.value
    property alias from: slider.from
    property alias to: slider.to
    property alias stepSize: slider.stepSize

    Text {
        id: label
        width: parent.width
        height: Units.px(20)
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        font.pixelSize: 20
        color: Colors.textSecondary
    }

    Slider {
        id: slider
        width: parent.width
        height: Units.px(24)
        snapMode: Slider.SnapAlways

        background: Rectangle {
            x: slider.leftPadding
            y: slider.topPadding + slider.availableHeight / 2 - height / 2
            width: slider.availableWidth
            height: Units.px(4) 
            radius: Units.px(2)
            color: Colors.layer01

            Rectangle {
                width: slider.visualPosition * parent.width
                height: parent.height
                radius: parent.radius
                color: slider.pressed ? Colors.buttonSecondaryActive : Colors.buttonSecondary
            }
        }

        handle: Rectangle {
            x: slider.leftPadding + slider.visualPosition * (slider.availableWidth - width)
            y: slider.topPadding + slider.availableHeight / 2 - height / 2
            width: radius * 2 
            height: radius * 2 
            radius: Units.px(8)
            color: slider.pressed ? Colors.buttonSecondaryActive : Colors.buttonSecondary
        }
    }
}
