import time
import logging
from pathlib import Path

from hslog import packets, LogParser

from cph.utils.logging import make_logger
from cph.game import power_log, exporter


def main():
    logger = make_logger('parse_power_log', logging.DEBUG)
    power_log_path: Path | None = None
    offset = 0
    parser = LogParser()
    prev_game: packets.PacketTree | None = None

    def read_line(line: str) -> None:
        parser.read_line(line)

    while True:
        power_log_path, offset = \
            power_log.handle_lines_once(read_line, power_log_path, offset)

        # preparation for queueing / incremental exporting
        # would not read the packets completely
        # but rather as they come
        current_game: packets.PacketTree = parser.games[-1]
        game_state_exporter = exporter.GameStateExporter(parser.player_manager, logger)
        for packet in current_game:
            game_state_exporter.export_packet(packet)
        game_state_exporter.flush()

        time.sleep(1)


if __name__ == '__main__':
    main()
