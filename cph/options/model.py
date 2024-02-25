from dataclasses import dataclass

@dataclass
class Option:
    suboptions: list['Option'] = []
    option: str | None = None

    def select(self, index: int) -> 'Option | None':
        try:
            return self.suboptions[index]
        except IndexError:
            return None

