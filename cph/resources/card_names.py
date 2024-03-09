import toml
from pathlib import Path


CARD_NAMES_PATH = Path('card_names.toml')


def save(card_names: dict[str, str]):
    with open(CARD_NAMES_PATH, 'w') as f:
        toml.dump(card_names, f)


def load() -> dict[str, str]:
    if not CARD_NAMES_PATH.exists():
        return {}
    with open(CARD_NAMES_PATH, 'r') as f:
        return toml.load(f)
