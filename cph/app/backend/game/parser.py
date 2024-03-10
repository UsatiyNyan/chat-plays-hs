import logging
from pathlib import Path
from datetime import datetime

from hslog import LogParser

from cph.game import power_log, exporter, handler


class PowerLogParser:
    def __init__(self, a_handler: handler.Handler, logger: logging.Logger):
        self._handler = a_handler
        self._logger = logger

        self._parser = LogParser()

        self._power_log_path: Path | None = None
        self._power_log_offset = 0

        self._exporter: exporter.Exporter | None = None
        self._ts: datetime | None = None

    def _read_line(self, line: str):
        self._parser.read_line(line)

    def parse_once(self):
        self._power_log_path, self._power_log_offset = \
            power_log.handle_lines_once(self._read_line,
                                        self._power_log_path,
                                        self._power_log_offset)

        self._exporter, self._ts = \
            exporter.handle_packets(self._parser,
                                    self._handler,
                                    self._logger,
                                    self._exporter,
                                    self._ts)
