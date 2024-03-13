from dataclasses import dataclass


# reflects option available for vote in chat
@dataclass
class VoteOption:
    option: str  # as in options
    alias: str   # key for chat
    votes: int = 0
