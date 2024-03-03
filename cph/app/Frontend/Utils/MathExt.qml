pragma Singleton
import QtQuick

QtObject {
    function safeFraction(num, den, defaultValue = 0) {
        if (den === 0) {
            return defaultValue;
        }
        return num / den;
    }
}
