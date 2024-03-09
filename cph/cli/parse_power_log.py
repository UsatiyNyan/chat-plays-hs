import time
import logging
from pathlib import Path

from hslog import LogParser

from cph.utils.logging import make_logger
from cph.game import power_log, exporter, state


def main():
    logger = make_logger('parse_power_log', logging.DEBUG)

    power_log_path: Path | None = None
    offset = 0
    parser = LogParser()

    game_state_exporter: exporter.GameStateExporter | None = None
    packet_offset = 0

    game_state = state.GameState(logger)

    def read_line(line: str) -> None:
        parser.read_line(line)

    while True:
        power_log_path, offset = \
            power_log.handle_lines_once(read_line, power_log_path, offset)

        game_state_exporter, packet_offset = exporter.handle_packets(
            parser, game_state, logger, game_state_exporter, packet_offset)
        time.sleep(1)


if __name__ == '__main__':
    main()
