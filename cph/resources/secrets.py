import toml
from dataclasses import dataclass


@dataclass
class Secrets:
    RAPID_API_KEY: str = ''
    TWITCH_ACCESS_TOKEN: str = ''


def load() -> Secrets:
    with open('secrets.toml') as f:
        return Secrets(**toml.load(f))
