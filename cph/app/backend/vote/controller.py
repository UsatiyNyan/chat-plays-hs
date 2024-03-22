import logging
from enum import IntEnum, auto
from typing import DefaultDict

from PySide6.QtCore import QObject, Property, Signal, Slot, QEnum, QTimer
from PySide6.QtQml import qmlRegisterType

from cph.utils.vec import Vec2

from cph.game.model import GameOption
from cph.game.board import Board, WindowBB, interact

from cph.vote.model import VoteOption
from cph.vote.interface import VoteInterface

from .model import VoteModel
from .misc import add_emote_option, remove_emote_option


class VoteState(IntEnum):
    Ready = auto()
    InProgress = auto()
    Finished = auto()


class VoteClientState(IntEnum):
    NotConnected = auto()
    Connected = auto()
    Error = auto()


class VoteController(QObject):
    QEnum(VoteState)
    QEnum(VoteClientState)

    voteSecondsLeftChanged = Signal()
    voteEmotesChanged = Signal()
    voteAutoModeChanged = Signal()
    voteSecondsTotalChanged = Signal()
    voteWinnerIndicesChanged = Signal()
    voteStateChanged = Signal()
    voteClientStateChanged = Signal()

    def __init__(self, logger: logging.Logger, parent=None):
        super().__init__(parent)
        self._logger = logger
        self._voteSecondsLeft = 10
        self._voteEmotes = True
        self._voteAutoMode = False
        self._voteSecondsTotal = 10
        self._voteWinnerIndices = []
        self._voteState = VoteState.Ready
        self._voteClientState = VoteClientState.NotConnected
        self._voteModel = VoteModel()

        self._interface = VoteInterface(self._logger)
        self._game_options: list[GameOption] = []
        self._max_count = 0

        # TODO: configurable BB
        self._window_bb = WindowBB(Vec2(0, 0), Vec2(1920, 1080))
        self._board: Board | None = None

        self._voteAutoModeTimer = QTimer(self)
        self._voteAutoModeTimer.timeout.connect(self.onVoteButtonClicked)
        self._voteAutoModeTimer.setSingleShot(True)
        self._voteAutoModeTimer.setInterval(2000)

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
            self.set_game_options(self._board, self._game_options, self._max_count)  # noqa

    @Property(bool, notify=voteAutoModeChanged)
    def voteAutoMode(self):
        return self._voteAutoMode

    @voteAutoMode.setter
    def voteAutoMode(self, value):
        if self._voteAutoMode != value:
            self._voteAutoMode = value
            self.voteAutoModeChanged.emit()

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

    def set_game_options(self, board: Board | None, game_options: list[GameOption], max_count: int = 1):
        if self.is_busy:
            self._logger.warn('set_game_options: busy')
            return

        self._board = board
        self._set_game_options(game_options, max_count)

    def _set_game_options(self, game_options: list[GameOption], max_count: int = 1):
        if self.voteEmotes:
            add_emote_option(game_options)
        else:
            remove_emote_option(game_options)

        self._game_options = game_options
        self._max_count = max_count
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

        if self.voteAutoMode and len(game_options) > 0 and \
                not self._voteAutoModeTimer.isActive():
            self._logger.info('[Auto mode] start vote in %d msec',
                              self._voteAutoModeTimer.interval())
            self._voteAutoModeTimer.start()

    def _start_vote(self):
        self.voteState = VoteState.InProgress
        self.voteSecondsLeft = self.voteSecondsTotal
        self.voteWinnerIndices = []
        self._interface.start()

        if self.voteAutoMode and self.voteSecondsTotal > 0:
            self._logger.info('[Auto mode] stop timer')
            self._voteAutoModeTimer.stop()

    def _stop_vote(self):
        self._fetch_votes()  # fetch votes one last time
        self.voteState = VoteState.Finished
        self.voteWinnerIndices = self._interface.stop()
        if not self.voteAutoMode:
            return
        for index in self._voteWinnerIndices:
            assert index >= 0 or index < len(self._game_options), \
                f'{len(self._game_options)=} {index=}'
            self.voteAutoMode = interact(self._logger,
                                         self._window_bb,
                                         self._board,
                                         self._game_options,
                                         index)

        if self.voteAutoMode:
            self._logger.info('[Auto mode] next vote in %d msec',
                              self._voteAutoModeTimer.interval())
            self._voteAutoModeTimer.start()

    def _prepare_vote(self):
        if len(self._voteWinnerIndices) != 1:
            self.voteState = VoteState.Ready
            self._set_game_options([])
            return

        index = self._voteWinnerIndices[0]
        if index < 0 or index >= len(self._game_options):
            self._logger.error(f'selected_option invalid index: {index}')
            return

        suboptions = self._game_options[index].suboptions
        if len(suboptions) == 0:
            self.voteState = VoteState.Ready
            self._set_game_options([])
            return

        self._set_game_options(suboptions)
        self._start_vote()
        if len(suboptions) == 1:
            self._stop_vote()

    def _fetch_votes(self):
        if self._voteState != VoteState.InProgress:
            return
        vote_options = self._interface.fetch()
        self._voteModel.update_votes(vote_options)

    @Property(int, notify=voteClientStateChanged)
    def voteClientState(self):
        return self._voteClientState

    @voteClientState.setter
    def voteClientState(self, value):
        if self._voteClientState != value:
            self._voteClientState = value
            self.voteClientStateChanged.emit()

    @Slot(str)
    def onVoteClientButtonClicked(self, url: str):
        match self._voteClientState:
            case VoteClientState.NotConnected:
                if self._interface.connect(url):
                    self.voteClientState = VoteClientState.Connected
                else:
                    self.voteClientState = VoteClientState.Error
            case VoteClientState.Connected:
                self._interface.disconnect()
                self.voteClientState = VoteClientState.NotConnected
            case VoteClientState.Error:
                self.voteClientState = VoteClientState.NotConnected
            case _:
                self._logger.error('VoteClientState is invalid')

    def close(self):
        self._interface.disconnect()


qmlRegisterType(VoteController, 'Frontend.Bindings', 1, 0, 'VoteController')
