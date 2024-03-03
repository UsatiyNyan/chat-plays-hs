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

    spacing: Units.px(16)

    Text {
        id: label
        width: parent.width
        height: Units.px(20)
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        font.pixelSize: 20
        color: Colors.textSecondary
    }

    Row {
        width: parent.width
        height: Units.px(24)

        Text {
            id: fromLabel
            width: Units.px(16)
            height: parent.height
            horizontalAlignment: Text.AlignLeft
            verticalAlignment: Text.AlignVCenter
            font.pixelSize: 16
            color: Colors.textHelper
            text: slider.from
        }

        Slider {
            id: slider
            width: parent.width - fromLabel.width - toLabel.width
            height: parent.height
            snapMode: Slider.SnapAlways

            background: Rectangle {
                x: slider.leftPadding
                y: slider.topPadding + slider.availableHeight / 2 - height / 2
                width: slider.availableWidth
                height: Units.px(4) 
                radius: Units.px(2)
                color: Colors.layer03

                Rectangle {
                    width: slider.visualPosition * parent.width
                    height: parent.height
                    radius: parent.radius
                    color: slider.pressed ? Colors.buttonPrimary : Colors.layerSelectedInverse
                }
            }

            handle: Rectangle {
                x: slider.leftPadding + slider.visualPosition * (slider.availableWidth - width)
                y: slider.topPadding + slider.availableHeight / 2 - height / 2
                width: radius * 2 
                height: radius * 2 
                radius: Units.px(8)
                color: slider.pressed ? Colors.buttonPrimary : Colors.layerSelectedInverse
            }
        }

        Text {
            id: toLabel
            width: Units.px(16)
            height: parent.height
            horizontalAlignment: Text.AlignRight
            verticalAlignment: Text.AlignVCenter
            font.pixelSize: 16
            color: Colors.textHelper
            text: slider.to
        }
    }
}
