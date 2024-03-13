import typing as t
import logging

from datetime import datetime
from dataclasses import dataclass


@dataclass
class VoteEntry:
    ts: datetime
    uid: int
    msg: str


class VoteClient:
    def start(self):
        pass

    def stop(self):
        pass

    def fetch(self) -> t.Iterable[VoteEntry]:
        pass


class LoggingVoteClient(VoteClient):
    def __init__(self, logger: logging.Logger):
        self._logger = logger

    def start(self):
        pass

    def stop(self):
        pass

    def fetch(self) -> t.Iterable[VoteEntry]:
        pass
