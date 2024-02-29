pragma Singleton
import QtQuick

QtObject {
    function svgPath(image) {
        return resourcesPath() + image + ".svg"
    }

    function pngPath(image) {
        return resourcesPath() + image + ".png"
    }

    function resourcesPath() {
        return "qrc:/resources/"
    }
}
