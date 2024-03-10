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

    @property
    def state(self) -> VoteState:
        return self._state

    def set_options(self, vote_options: list[VoteOption], max_count: int = 1):
        pass

    def on_vote_button_clicked(self):
        pass
