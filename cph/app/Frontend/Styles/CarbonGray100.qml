import QtQuick

QtObject {
    // colors
    readonly property color white: "#ffffff"

    readonly property color gray10: "#f4f4f4"
    readonly property color gray20: "#e0e0e0"
    readonly property color gray30: "#c6c6c6"
    readonly property color gray40: "#a8a8a8"
    readonly property color gray50: "#8d8d8d"
    readonly property color gray60: "#6f6f6f"
    readonly property color gray70: "#525252"
    readonly property color gray80: "#393939"
    readonly property color gray90: "#262626"
    readonly property color gray100: "#161616"
    readonly property color gray10Hover: "#e5e5e5"
    readonly property color gray60Hover: "#606060"
    readonly property color gray70Hover: "#636363"
    readonly property color gray80Hover: "#474747"
    readonly property color gray90Hover: "#333333"

    readonly property color red40: "#ff8389"
    readonly property color red50: "#fa4d56"
    readonly property color red60: "#da1e28"
    readonly property color red60Hover: "#ba1b23"
    readonly property color red80: "#750e13"

    readonly property color blue50: "#4589ff"
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
    readonly property color backgroundBrand: blue60

    // layer
    readonly property color layer01: gray90
    readonly property color layer02: gray80
    readonly property color layer03: gray70
    readonly property color layer01Hover: gray90Hover
    readonly property color layer02Hover: gray80Hover
    readonly property color layer03Hover: gray70Hover
    readonly property color layer01Active: gray70
    readonly property color layer02Active: gray60
    readonly property color layer03Active: gray50
    readonly property color layer01Selected: gray80
    readonly property color layer02Selected: gray70
    readonly property color layer03Selected: gray60
    readonly property color layer01SelectedHover: gray80Hover
    readonly property color layer02SelectedHover: gray70Hover
    readonly property color layer03SelectedHover: gray60Hover
    readonly property color layerSelectedInverse: gray10
    readonly property color layerSelectedDisabled: gray60

    // layer accent
    readonly property color layerAccent01: gray80
    readonly property color layerAccent02: gray70
    readonly property color layerAccent03: gray60
    readonly property color layerAccentHover01: gray80Hover
    readonly property color layerAccentHover02: gray70Hover
    readonly property color layerAccentHover03: gray60Hover
    readonly property color layerAccentActive01: gray70
    readonly property color layerAccentActive02: gray50
    readonly property color layerAccentActive03: gray80

    // field
    readonly property color field01: gray90
    readonly property color field02: gray80
    readonly property color field03: gray70
    readonly property color field01Hover: gray90Hover
    readonly property color field02Hover: gray80Hover
    readonly property color field03Hover: gray70Hover

    // border
    readonly property color borderInteractive: blue50
    readonly property color borderSubtle00: gray80
    readonly property color borderSubtle01: gray80
    readonly property color borderSubtle02: gray70
    readonly property color borderSubtle03: gray60
    readonly property color borderSubtleSelected01: gray70
    readonly property color borderSubtleSelected02: gray60
    readonly property color borderSubtleSelected03: gray60
    readonly property color borderStrong01: gray60
    readonly property color borderStrong02: gray50
    readonly property color borderStrong03: gray40
    readonly property color borderTile01: gray70
    readonly property color borderTile02: gray60
    readonly property color borderTile03: gray50
    readonly property color borderInverse: gray10
    readonly property color borderDisabled: Qt.alpha(gray50, 0.5)

    // text
    readonly property color textPrimary: gray10
    readonly property color textSecondary: gray30
    readonly property color textPlaceholder: gray60
    readonly property color textOnColor: white
    readonly property color textOnColorDisabled: Qt.alpha(white, 0.25)
    readonly property color textHelper: gray50
    readonly property color textError: red40
    readonly property color textInverse: gray100
    readonly property color textDisabled: Qt.alpha(gray10, 0.25)

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
