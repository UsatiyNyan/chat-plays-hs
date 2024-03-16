import typing as t
import logging

import urllib.parse
from datetime import datetime
from dataclasses import dataclass

from .model import VoteOption


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

    def start(self, vote_options: list[VoteOption], max_count: int):
        self._logger.info('VoteClient started, '
                          f'options: {vote_options}, max_count: {max_count}')

    def stop(self, winners: list[VoteOption]):
        self._logger.info(f'VoteClient stopped, winners: {winners}')

    def fetch(self) -> t.Iterable[VoteEntry]:
        self._logger.info('VoteClient fetched')
        return []
