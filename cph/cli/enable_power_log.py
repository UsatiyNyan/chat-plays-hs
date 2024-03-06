import logging
from cph.utils.logging import make_logger
from cph.game import log_config


def main():
    logger = make_logger('enable_power_log', logging.INFO)

    log_config_path = log_config.get_path()
    if log_config_path is None:
        logger.error('log_config_path is None')
        return
    logger.info(f'{log_config_path=} exists={log_config_path.exists()}')

    log_config.power_enable()

    logger.info('Power log enabled, restart Hearthstone to see the logs.')


if __name__ == '__main__':
    main()
