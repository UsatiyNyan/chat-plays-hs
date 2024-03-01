import QtQuick

QtObject {
    // colors
    readonly property color white: "#ffffff"

    readonly property color gray10: "#f4f4f4"
    readonly property color gray10Hover: "#e5e5e5"
    readonly property color gray30: "#c6c6c6"
    readonly property color gray50: "#8d8d8d"
    readonly property color gray60: "#6f6f6f"
    readonly property color gray60Hover: "#606060"
    readonly property color gray70: "#525252"
    readonly property color gray80: "#393939"
    readonly property color gray100: "#161616"

    readonly property color red50: "#fa4d56"
    readonly property color red60: "#da1e28"
    readonly property color red60Hover: "#ba1b23"
    readonly property color red80: "#750e13"

    readonly property color blue60: "#0f62fe"
    readonly property color blue60Hover: "#0353e9"
    readonly property color blue80: "#002d9c"

    // background
    readonly property color background: gray100
    readonly property color backgroundHover: Qt.alpha(gray50, 0.16)
    readonly property color backgroundActive: Qt.alpha(gray50, 0.40)
    readonly property color backgroundSelected: Qt.alpha(gray50, 0.24)
    readonly property color backgroundSelectedHover: Qt.alpha(gray50, 0.32)
    readonly property color backgroundInverse: gray10
    readonly property color backgroundInverseHover: gray10Hover

    // icon
    readonly property color iconPrimary: gray10
    readonly property color iconSecondary: gray30
    readonly property color iconOnColor: white
    readonly property color iconOnColorDisabled: Qt.alpha(white, 0.25)
    readonly property color iconInteractive: white
    readonly property color iconInverse: gray100
    readonly property color iconDisabled: Qt.alpha(gray10, 0.25)

    // button
    readonly property color buttonPrimary: blue60
    readonly property color buttonPrimaryHover: blue60Hover
    readonly property color buttonPrimaryActive: blue80

    readonly property color buttonSecondary: gray60
    readonly property color buttonSecondaryHover: gray60Hover
    readonly property color buttonSecondaryActive: gray80

    readonly property color buttonTertiary: white
    readonly property color buttonTertiaryHover: gray10
    readonly property color buttonTertiaryActive: gray30

    readonly property color buttonDangerPrimary: red60
    readonly property color buttonDangerSecondary: red50
    readonly property color buttonDangerHover: red60Hover
    readonly property color buttonDangerActive: red80

    readonly property color buttonSeparator: gray100
    readonly property color buttonDisabled: gray70
}
