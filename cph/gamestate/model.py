from dataclasses import dataclass


@dataclass
class GameOption:
    option: str
    group: str
    suboptions: list['GameOption'] = []

    def select(self, index: int) -> 'GameOption | None':
        try:
            return self.suboptions[index]
        except IndexError:
            return None

    def make_alias(self, index: int) -> str:
        group_alias = self.group[0].lower()
        return f"{group_alias}{index}"
