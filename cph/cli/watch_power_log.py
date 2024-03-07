import time
from pathlib import Path
from cph.game import power_log


def main():
    power_log_path: Path | None = None
    offset = 0
    while True:
        power_log_path, offset = \
            power_log.handle_lines_once(print, power_log_path, offset)
        time.sleep(1)


if __name__ == '__main__':
    main()
