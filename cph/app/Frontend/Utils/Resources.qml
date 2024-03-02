pragma Singleton
import QtQuick

QtObject {
    function resourcesRoot() {
        return 'qrc:/resources/'
    }

    function image(imageName) {
        return resourcesRoot() + 'images/' + imageFile + '.png'
    }

    function icon(iconName) {
        return resourcesRoot() + 'icons/' + iconName + '.svg'
    }

    function font(fontName) {
        return resourcesRoot() + 'fonts/' + fontName + '.ttf'
    }
}
