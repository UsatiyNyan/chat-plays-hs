from enum import Enum, auto


class VoteState(Enum):
    NotStarted = auto()
    InProgress = auto()
    Finished = auto()
