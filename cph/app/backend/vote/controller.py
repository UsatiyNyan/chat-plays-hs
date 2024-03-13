import logging
from enum import IntEnum, auto
from typing import DefaultDict

from PySide6.QtCore import QObject, Property, Signal, Slot, QEnum
from PySide6.QtQml import qmlRegisterType

from cph.game.model import GameOption
from cph.vote.model import VoteOption
from cph.vote.interface import VoteInterface

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
    voteWinnerIndicesChanged = Signal()
    voteStateChanged = Signal()

    def __init__(self, logger: logging.Logger, parent=None):
        super().__init__(parent)
        self._logger = logger
        self._voteSecondsLeft = 10
        self._voteEmotes = True
        self._voteSecondsTotal = 10
        self._voteWinnerIndices = []
        self._voteState = VoteState.Ready
        self._voteModel = VoteModel()
        self._interface = VoteInterface(self._logger)

        self._game_options: list[GameOption] = []

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

    @Property(list, notify=voteWinnerIndicesChanged)
    def voteWinnerIndices(self):
        return self._voteWinnerIndices

    @voteWinnerIndices.setter
    def voteWinnerIndices(self, value):
        if self._voteWinnerIndices != value:
            self._voteWinnerIndices = value
            self.voteWinnerIndicesChanged.emit()

    @Property(int, notify=voteStateChanged)
    def voteState(self):
        return self._voteState

    @voteState.setter
    def voteState(self, value):
        if self._voteState != value:
            self._voteState = value
            self.voteStateChanged.emit()

    @property
    def is_busy(self) -> bool:
        return self._voteState != VoteState.Ready

    @Slot()
    def onVoteButtonClicked(self):
        match self._voteState:
            case VoteState.Ready:
                self._start_vote()
            case VoteState.InProgress:
                self._stop_vote()
            case VoteState.Finished:
                self._prepare_vote()
            case _:
                self._logger.error('VoteState is invalid')

    def tick(self):
        if self._voteState != VoteState.InProgress:
            return

        self._fetch_votes()

        if self._voteSecondsTotal <= 0:
            return

        self.voteSecondsLeft -= 1
        if self._voteSecondsLeft > 0:
            return

        self._stop_vote()

    def set_game_options(self, game_options: list[GameOption], max_count: int = 1):
        if self.is_busy:
            self._logger.warn('set_game_options: busy')
            return

        self._set_game_options(game_options, max_count)

    def _set_game_options(self, game_options: list[GameOption], max_count: int = 1):
        self._game_options = game_options
        group_indices: DefaultDict[str, int] = DefaultDict(int)
        vote_options = []
        for game_option in game_options:
            group_indices[game_option.group] += 1
            index = group_indices[game_option.group]
            vote_options.append(
                VoteOption(
                    option=game_option.option,
                    alias=game_option.make_alias(index),
                    votes=0,
                )
            )
        self._voteModel.set_options(game_options, vote_options)
        self._interface.set_options(vote_options, max_count)

    def _start_vote(self):
        self.voteState = VoteState.InProgress
        self.voteSecondsLeft = self.voteSecondsTotal
        self._interface.start()

    def _stop_vote(self):
        self._fetch_votes()  # fetch votes one last time
        self.voteState = VoteState.Finished
        self.winnerIndices = self._interface.stop()

    def _prepare_vote(self):
        self.voteState = VoteState.Ready
        if len(self._voteWinnerIndices) != 1:
            return

        index = self._voteWinnerIndices[0]
        if index < 0 or index >= len(self._game_options):
            self._logger.error(f'selected_option invalid index: {index}')
            return

        suboptions = self._game_options[index].suboptions
        self._set_game_options(suboptions)

    def _fetch_votes(self):
        if self._voteState != VoteState.InProgress:
            return
        vote_options = self._interface.fetch()
        self._voteModel.update_votes(vote_options)


qmlRegisterType(VoteController, 'Frontend.Bindings', 1, 0, 'VoteController')
