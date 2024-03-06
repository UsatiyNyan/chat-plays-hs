import os
import logging
import toml
from pathlib import Path

from cph.utils.logging import make_logger


def load_log_config(log_config_path: Path) -> dict:
    if not log_config_path.exists():
        return {}
    with log_config_path.open('r') as log_config_file:
        return toml.load(log_config_file)


def dump_log_config(log_config: dict, log_config_path: Path):
    with log_config_path.open('w') as log_config_file:
        toml.dump(log_config, log_config_file)


def log_config_options() -> dict:
    return {
        'LogLevel': 1,
        'FilePrinting': True,
        'ConsolePrinting': False,
        'ScreenPrinting': False,
        'Verbose': True
    }


def main():
    logger = make_logger('enable_power_log', logging.INFO)

    local_app_data = os.getenv('LocalAppData')
    if local_app_data is None:
        logger.error('LocalAppData environment variable is not set')
        return
    logger.info(f'{local_app_data=}')

    log_config_path = Path(local_app_data, 'Blizzard',
                           'Hearthstone', 'log.config')
    logger.info(f'{log_config_path=} exists={log_config_path.exists()}')

    log_config = load_log_config(log_config_path)
    log_config['Power'] = log_config_options()
    dump_log_config(log_config, log_config_path)

    logger.info('Power log enabled, restart Hearthstone to see the logs.')


if __name__ == '__main__':
    main()
