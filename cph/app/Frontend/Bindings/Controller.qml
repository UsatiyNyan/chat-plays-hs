import QtQuick

QtObject {
    readonly property var voteController: VoteController {}
    readonly property var gameController: GameController {}

    function close() {
        console.log('Close Controller')
        voteController.close()
        gameController.close()
    }
}
