from PySide6.QtCore import QObject, Property, Signal, Slot
from PySide6.QtQml import qmlRegisterType

from cph.app.backend.options.model import DisplayOptionsModel


class DisplayOptionsController(QObject):
    # Signals for property changes
    voteSecondsLeftChanged = Signal()
    voteEmotesChanged = Signal()
    voteSecondsTotalChanged = Signal()
    voteWinnerIndexChanged = Signal()
    voteWinnerHasCandidatesChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._voteSecondsLeft = 10
        self._voteEmotes = True
        self._voteSecondsTotal = 10
        self._voteWinnerIndex = -1
        self._voteWinnerHasCandidates = True
        self._voteModel = DisplayOptionsModel()

    # Property getters and setters
    @Property(DisplayOptionsModel, constant=True)
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

    @Property(bool, notify=voteWinnerHasCandidatesChanged)
    def voteWinnerHasCandidates(self):
        return self._voteWinnerHasCandidates

    @voteWinnerHasCandidates.setter
    def voteWinnerHasCandidates(self, value):
        if self._voteWinnerHasCandidates != value:
            self._voteWinnerHasCandidates = value
            self.voteWinnerHasCandidatesChanged.emit()

    @Slot()
    def onVoteButtonClicked(self):
        print('Vote button clicked')
        # TODO


qmlRegisterType(DisplayOptionsController,
                'Frontend.Bindings', 1, 0, 'VoteController')
