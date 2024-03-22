import time
import logging
from cph.utils.logging import make_logger
from cph.app.backend.game.parser import PowerLogParser
from cph.game.handler import Handler


def main():
    logger = make_logger('parse_power_log', logging.DEBUG)
    handler = Handler(logger)
    parser = PowerLogParser(handler, logger)

    while True:
        parser.parse_once()
        time.sleep(1)


if __name__ == '__main__':
    main()
