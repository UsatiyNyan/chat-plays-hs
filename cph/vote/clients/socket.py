import typing as t
import logging
import socket
import urllib.parse

from enum import Enum, auto
from datetime import datetime, UTC
from cph.utils.generator import is_not_none

from cph.vote.client import VoteClient, VoteEntry


class SocketClientState(Enum):
    HasData = auto()
    NoData = auto()
    Disconnected = auto()


class SocketVoteClient(VoteClient):
    def __init__(self, logger: logging.Logger):
        super().__init__(logger)
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client: socket.socket | None = None

    def connect(self, url: urllib.parse.ParseResult) -> bool:
        host, port = url.scheme, url.path
        try:
            self._server.bind((host, int(port)))
        except Exception:
            return False

        self._server.setblocking(False)
        self._server.listen(1)
        self._logger.info(f'VoteClient server started at {host}:{port}')
        return True

    def disconnect(self):
        if self._client is not None:
            self._client.close()
            self._client = None
        self._server.close()

    def start(self):
        super().start()
        if self._client is None:
            try:
                self._client, addr = self._server.accept()
                self._logger.info(f'VoteClient connected by {addr}')
            except BlockingIOError:
                self._logger.warning('VoteClient not connected')

    def stop(self):
        super().stop()

    def fetch(self) -> t.Iterable[VoteEntry]:
        if self._client is None:
            return []

        entries: list[VoteEntry] = []
        while True:
            data, client_state = self._retrieve_data(self._client)
            match client_state:
                case SocketClientState.HasData:
                    maybe_entries = map(self._parse_entry, data.split('\n'))
                    entries.extend(filter(is_not_none, maybe_entries))
                case SocketClientState.NoData:
                    break
                case SocketClientState.Disconnected:
                    self._client.close()
                    self._client = None
                    break

        return entries

    def _retrieve_data(self, conn: socket.socket) -> t.Tuple[str, SocketClientState]:
        try:
            data = conn.recv(1024)
            if not data:
                return '', SocketClientState.Disconnected
            return data.decode('utf-8'), SocketClientState.HasData
        except BlockingIOError:
            return '', SocketClientState.NoData
        except ConnectionResetError:
            return '', SocketClientState.Disconnected

    def _parse_entry(self, msg: str) -> VoteEntry | None:
        if not msg:
            return None

        uid_and_msg = msg.split(':')
        if len(uid_and_msg) != 2:
            self._logger.error(f'VoteClient received invalid message: {msg}')
            return None

        uid, msg = uid_and_msg
        vote_entry = VoteEntry(datetime.now(tz=UTC), uid, msg)
        self._logger.info(f'VoteClient received: {vote_entry}')
        return vote_entry
