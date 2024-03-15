import typing as t
import logging
import socket

from enum import Enum, auto
from datetime import datetime, UTC

from cph.vote.client import VoteClient, VoteEntry


class SocketClientState(Enum):
    HasData = auto()
    NoData = auto()
    Disconnected = auto()


class SocketVoteClient(VoteClient):
    def __init__(self, logger: logging.Logger):
        super().__init__(logger)
        self._server = self._create_server()
        self._client: socket.socket | None = None

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
            vote_entry, client_state = self._serve_client(self._client)
            match client_state:
                case SocketClientState.HasData:
                    if vote_entry is not None:
                        entries.append(vote_entry)
                case SocketClientState.NoData:
                    break
                case SocketClientState.Disconnected:
                    self._client.close()
                    self._client = None
                    break

        return entries

    def _create_server(self) -> socket.socket:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setblocking(False)
        host = socket.gethostname()
        port = 13131
        server_socket.bind((host, port))
        server_socket.listen(1)
        self._logger.info(f'VoteClient server started at {host}:{port}')
        return server_socket

    def _serve_client(self, conn: socket.socket) \
            -> t.Tuple[VoteEntry | None, SocketClientState]:
        try:
            data = conn.recv(1024)
            if not data:
                return None, SocketClientState.Disconnected
        except BlockingIOError:
            return None, SocketClientState.NoData
        except ConnectionResetError:
            return None, SocketClientState.Disconnected

        msg = data.decode('utf-8')
        uid_and_msg = msg.split(':')
        if len(uid_and_msg) != 2:
            self._logger.error(f'VoteClient received invalid message: {msg}')
            return None, SocketClientState.HasData

        uid, msg = uid_and_msg
        vote_entry = VoteEntry(datetime.now(tz=UTC), uid, msg)
        self._logger.info(f'VoteClient received: {vote_entry}')
        return vote_entry, SocketClientState.HasData
