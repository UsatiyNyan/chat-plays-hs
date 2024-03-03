import QtQuick

ListModel {
    property int votesSum: 300
    property int votesMax: 100
    ListElement {
        group: 'Hand'
        alias: 'H1'
        option: 'Shiv'
        votes: 20
    }
    ListElement {
        group: 'Hand'
        alias: 'H2'
        option: 'Backstab'
        votes: 10
    }
    ListElement {
        group: 'Play'
        alias: 'P1'
        option: 'Valeera'
        votes: 50
    }
    ListElement {
        group: 'Play'
        alias: 'P2'
        option: 'Patches the Pirate'
        votes: 30
    }
    ListElement {
        group: 'Misc'
        alias: 'M1'
        option: 'End Turn'
        votes: 10
    }
    ListElement {
        group: 'Misc'
        alias: 'M2'
        option: 'Concede'
        votes: 100
    }
    ListElement {
        group: 'Misc'
        alias: 'M3'
        option: 'Emote'
        votes: 80
    }
}

