import typing as t
import logging

import urllib.parse
from datetime import datetime
from dataclasses import dataclass


@dataclass
class VoteEntry:
    ts: datetime
    uid: str
    msg: str


class VoteClient:
    def __init__(self, logger: logging.Logger):
        self._logger = logger

    def connect(self, url: urllib.parse.ParseResult) -> bool:
        pass

    def disconnect(self):
        pass

    def start(self):
        self._logger.info('VoteClient started')

    def stop(self):
        self._logger.info('VoteClient stopped')

    def fetch(self) -> t.Iterable[VoteEntry]:
        self._logger.info('VoteClient fetched')
        return []
