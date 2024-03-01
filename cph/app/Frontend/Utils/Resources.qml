pragma Singleton
import QtQuick

QtObject {
    function resourcesRoot() {
        return "qrc:/resources/"
    }

    function imagePath(imageFile) {
        return resourcesRoot() + "images/" + imageFile
    }
}
