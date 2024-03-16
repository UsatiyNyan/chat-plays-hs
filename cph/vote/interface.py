import typing as t
import logging
import urllib.parse
from datetime import datetime, UTC

from cph.resources import secrets
from cph.utils.generator import is_not_none

from .model import VoteOption
from .client import VoteClient, VoteEntry
from .clients import SocketVoteClient, TwitchVoteClient
from .prepare import parse_vote, calc_vote_weight, choose_winners


class VoteInterface:
    def __init__(self, logger: logging.Logger):
        self._logger = logger
        self._secrets: secrets.Secrets = secrets.load()
        self._client: VoteClient | None = None

        self._max_count: int = 0
        self._vote_options: list[VoteOption] = []
        self._vote_aliases: dict[str, int] = {}

        self._uids_voted: set[str] = set()
        self._ts_begin: datetime | None = None

    def connect(self, url_str: str) -> bool:
        url = urllib.parse.urlparse(url_str)
        self._client = self._make_client(url)
        if self._client is None:
            return False
        return self._client.connect(url)

    def _make_client(self, url: urllib.parse.ParseResult) -> VoteClient | None:
        match url.scheme:
            case 'https':
                match url.netloc:
                    case 'www.twitch.tv':
                        return TwitchVoteClient(
                                url.path.lstrip('/'),
                                self._secrets,
                                self._logger)
            case 'localhost':
                return SocketVoteClient(self._logger)
            case _:
                self._logger.error(
                    f'VoteInterface: unknown scheme {url.scheme}')
                return None

    def disconnect(self):
        if self._client is not None:
            self._client.disconnect()

    def set_options(self, vote_options: list[VoteOption], max_count: int):
        self._max_count = max_count
        self._vote_options = vote_options
        self._vote_aliases = {
            vote_option.alias: index for index, vote_option in enumerate(vote_options)
        }

    def start(self):
        self._uids_voted.clear()
        self._ts_begin = datetime.now(tz=UTC)
        if self._client is not None:
            self._client.start(self._vote_options, self._max_count)

    def stop(self) -> list[int]:
        winner_indices = choose_winners(self._vote_options, self._max_count)
        winners = [self._vote_options[index] for index in winner_indices]
        if self._client is not None:
            self._client.stop(winners)
        return winner_indices

    def fetch(self) -> list[VoteOption]:
        if self._client is None:
            return []

        for vote_aliases in self._parse_votes(self._client.fetch()):
            vote_indices: list[int] = \
                list(filter(is_not_none, map(self._vote_aliases.get, vote_aliases)))
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
