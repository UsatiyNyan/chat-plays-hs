from enum import IntEnum, auto

from PySide6.QtCore import QObject, Property, Signal, Slot, QEnum
from PySide6.QtQml import qmlRegisterType

from .model import VoteModel


class VoteState(IntEnum):
    Ready = auto()
    InProgress = auto()
    Finished = auto()


class VoteController(QObject):
    QEnum(VoteState)

    voteSecondsLeftChanged = Signal()
    voteEmotesChanged = Signal()
    voteSecondsTotalChanged = Signal()
    voteWinnerIndexChanged = Signal()
    voteStateChanged = Signal()

    def __init__(self, on_vote_button_clicked, parent=None):
        super().__init__(parent)
        self._voteSecondsLeft = 10
        self._voteEmotes = True
        self._voteSecondsTotal = 10
        self._voteWinnerIndex = -1
        self._voteState = VoteState.Ready
        self._voteModel = VoteModel()
        self._onVoteButtonClicked = on_vote_button_clicked

    @Property(VoteModel, constant=True)
    def voteModel(self):
        return self._voteModel

    @Property(int, notify=voteSecondsLeftChanged)
    def voteSecondsLeft(self):
        return self._voteSecondsLeft

    @voteSecondsLeft.setter
    def voteSecondsLeft(self, value):
        if self._voteSecondsLeft != value:
            self._voteSecondsLeft = value
            self.voteSecondsLeftChanged.emit()

    @Property(bool, notify=voteEmotesChanged)
    def voteEmotes(self):
        return self._voteEmotes

    @voteEmotes.setter
    def voteEmotes(self, value):
        if self._voteEmotes != value:
            self._voteEmotes = value
            self.voteEmotesChanged.emit()

    @Property(int, notify=voteSecondsTotalChanged)
    def voteSecondsTotal(self):
        return self._voteSecondsTotal

    @voteSecondsTotal.setter
    def voteSecondsTotal(self, value):
        if self._voteSecondsTotal != value:
            self._voteSecondsTotal = value
            self.voteSecondsTotalChanged.emit()

    @Property(int, notify=voteWinnerIndexChanged)
    def voteWinnerIndex(self):
        return self._voteWinnerIndex

    @voteWinnerIndex.setter
    def voteWinnerIndex(self, value):
        if self._voteWinnerIndex != value:
            self._voteWinnerIndex = value
            self.voteWinnerIndexChanged.emit()

    @Property(int, notify=voteStateChanged)
    def voteState(self):
        return self._voteState

    @voteState.setter
    def voteState(self, value):
        if self._voteState != value:
            self._voteState = value
            self.voteStateChanged.emit()

    @Slot()
    def onVoteButtonClicked(self):
        self._onVoteButtonClicked()


qmlRegisterType(VoteController, 'Frontend.Bindings', 1, 0, 'VoteController')
