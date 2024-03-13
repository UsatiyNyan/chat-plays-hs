import typing as t
import logging
from datetime import datetime, UTC

from .model import VoteOption
from .client import VoteClient, VoteEntry
from .prepare import parse_vote, calc_vote_weight, choose_winners


class VoteInterface:
    def __init__(self, logger: logging.Logger):
        self._logger = logger
        self._client = VoteClient()

        self._max_count: int = 0
        self._vote_options: list[VoteOption] = []
        self._vote_aliases: dict[str, int] = {}

        self._uids_voted: set[int] = set()
        self._ts_begin: datetime | None = None

    def set_options(self, vote_options: list[VoteOption], max_count: int):
        self._max_count = max_count
        self._vote_options = vote_options
        self._vote_aliases = {
            vote_option.alias: index for index, vote_option in enumerate(vote_options)
        }

    def start(self):
        self._uids_voted.clear()
        self._ts_begin = datetime.now(tz=UTC)
        self._client.start()

    def stop(self) -> list[int]:
        self._client.stop()
        return choose_winners(self._vote_options, self._max_count)

    def fetch(self) -> list[VoteOption]:
        for vote_aliases in self._parse_votes(self._client.fetch()):
            vote_indices = list(filter(None, map(self._vote_aliases.get, vote_aliases)))
            vote_weight = calc_vote_weight(vote_indices)
            for vote_index in vote_indices:
                self._vote_options[vote_index].votes += vote_weight

        return self._vote_options

    def _parse_votes(self, entries: t.Iterable[VoteEntry]) -> t.Iterable[list[str]]:
        if self._ts_begin is None:
            self._logger.error('vote not started')
            return

        for entry in entries:
            if entry.ts < self._ts_begin:
                continue

            vote_aliases = parse_vote(entry.msg)
            if vote_aliases is None:
                continue

            if entry.uid in self._uids_voted:
                continue

            self._uids_voted.add(entry.uid)
            yield vote_aliases
