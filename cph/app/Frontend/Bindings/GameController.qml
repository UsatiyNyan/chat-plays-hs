import QtQuick

QtObject {
    property bool isPowerLogEnabled: false

    function enablePowerLog() {
        if (isPowerLogEnabled) {
            console.log('Power log is already enabled')
            return
        }
        console.log('Enabling power log')
        isPowerLogEnabled = true
    }
}
