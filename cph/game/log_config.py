import os
import toml
from pathlib import Path


def get_path() -> Path | None:
    local_app_data = os.getenv('LocalAppData')
    if local_app_data is None:
        return None
    return Path(local_app_data, 'Blizzard', 'Hearthstone', 'log.config')


def load(path: Path) -> dict:
    if not path.exists():
        return {}
    with path.open('r') as file:
        return toml.load(file)


def dump(log_config: dict, path: Path):
    with path.open('w') as file:
        toml.dump(log_config, file)


def power_default_options() -> dict:
    return {
        'LogLevel': 1,
        'FilePrinting': True,
        'ConsolePrinting': False,
        'ScreenPrinting': False,
        'Verbose': True
    }


def power_enable() -> bool:
    path = get_path()
    if path is None:
        return False
    log_config = load(path)
    log_config['Power'] = power_default_options()
    dump(log_config, path)
    return True


def power_is_enabled() -> bool:
    path = get_path()
    if path is None:
        return False
    log_config = load(path)
    power = log_config.get('Power', {})
    return power.get('LogLevel') == 1 and \
        power.get('FilePrinting') and \
        power.get('Verbose')
