import logging
from cph.utils.logging import make_logger
from cph.game import power_log


def main():
    logger = make_logger('find_power_log', logging.INFO)

    power_log_path = power_log.get_path()
    if power_log_path is None:
        logger.error('power_log_path is None')
        return
    logger.info(f'{power_log_path=} exists={power_log_path.exists()}')
    with power_log_path.open('r') as file:
        for line, _ in zip(file, range(10)):
            print(line.strip())


if __name__ == '__main__':
    main()
