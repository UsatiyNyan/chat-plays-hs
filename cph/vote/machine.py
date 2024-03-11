import typing as t
import logging

from .state import VoteState
from .model import VoteOption


class VoteMachine:
    def __init__(self, logger: logging.Logger):
        self._logger = logger

        self.on_update_votes: t.Callable[[list[VoteOption]], None] = \
            lambda _: None
        self.on_selected_winners: t.Callable[[list[int]], None] = \
            lambda _: None
        self.on_proceed_with_option: t.Callable[[int], None] = \
            lambda _: None

        self._state = VoteState.NotStarted

        self._seconds_total = 0
        self._seconds_left = 0

    @property
    def state(self) -> VoteState:
        return self._state

    @property
    def is_busy(self) -> bool:
        return self._state != VoteState.NotStarted

    def _start_vote(self, seconds_total: int):
        self._state = VoteState.InProgress
        self._seconds_total = seconds_total
        self._seconds_left = seconds_total

    def _stop_vote(self):
        self._state = VoteState.Finished
        # TODO: stop vote, next state, show winners
        self._state = VoteState.Finished
        self.on_selected_winners(...)  # TODO

    def _prepare_vote(self):
        self._state = VoteState.NotStarted
        self.on_proceed_with_option(...)  # TODO

    def _fetch_votes(self):
        self.on_update_votes(...)  # TODO

    def set_options(self, vote_options: list[VoteOption], max_count: int = 1):
        pass

    def on_vote_button_clicked(self, seconds_total: int):
        match self._state:
            case VoteState.NotStarted:
                self._start_vote(seconds_total)
            case VoteState.InProgress:
                self._stop_vote()
            case VoteState.Finished:
                self._prepare_vote()
            case _:
                self._logger.warning('Vote already in progress')

    def tick(self) -> int:
        if self._state != VoteState.InProgress:
            return 0
        self._fetch_votes()
        if self._seconds_total <= 0:
            return 0
        self._seconds_left -= 1
        if self._seconds_left <= 0:
            self._stop_vote()
            return 0
        return self._seconds_left
