from dataclasses import dataclass

from hearthstone.enums import Zone


@dataclass
class GameOption:
    option: str
    group: str
    suboptions: list['GameOption']

    def select(self, index: int) -> 'GameOption | None':
        try:
            return self.suboptions[index]
        except IndexError:
            return None

    def make_alias(self, index: int) -> str:
        group_alias = self.group[0].upper() if len(self.group) > 0 else 'U'
        return f"{group_alias}{index}"

    @staticmethod
    def make_group(zone: int):
        match zone:
            case Zone.HAND:
                return 'Hand'
            case Zone.PLAY:
                return 'Play'
            case _:
                return 'Misc'


def load_card_names() -> dict[str, str]:
    # TODO: card names instead of card ids
    return {}
