import typing as t
import logging
import socket

from datetime import datetime, UTC
from threading import Thread, Lock

from cph.vote.client import VoteClient, VoteEntry


class StubVoteClient(VoteClient):
    def __init__(self, logger: logging.Logger):
        super().__init__(logger)
        self._entries: list[VoteEntry] = []
        self._entries_lock = Lock()

        self._server_thread = Thread(target=self._server)
        self._server_thread.start()

    def start(self):
        super().start()

    def stop(self):
        super().stop()

    def fetch(self) -> t.Iterable[VoteEntry]:
        with self._entries_lock:
            entries = self._entries
            self._entries = []
        return entries

    def _server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()
        port = 13131
        server_socket.bind((host, port))
        server_socket.listen(1)
        self._logger.info(f'VoteClient server started at {host}:{port}')

        conn, addr = server_socket.accept()
        self._logger.info(f'VoteClient connected by {addr}')

        try:
            with conn:
                while self._server_thread.is_alive() and self._serve_client(conn):
                    pass
        except ConnectionResetError:
            self._logger.error('Connection reset')
        except Exception as e:
            self._logger.error(f'Error: {e}')
        finally:
            self._logger.info('Client disconnected')

    def _serve_client(self, conn):
        data = conn.recv(1024)
        if not data:
            return False

        msg = data.decode('utf-8')
        uid_and_msg = msg.split(':')
        if len(uid_and_msg) != 2:
            self._logger.error(
                f'VoteClient received invalid message: {msg}')
            return True

        uid, msg = uid_and_msg
        vote_entry = VoteEntry(datetime.now(tz=UTC), uid, msg)
        with self._entries_lock:
            self._entries.append(vote_entry)

        self._logger.info(f'VoteClient received: {vote_entry}')
        return True
