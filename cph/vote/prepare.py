import re

from itertools import islice
from functools import reduce
from operator import mul

from .model import VoteOption


class VoteConstants:
    MAX_VOTE_OPTIONS = 4
    MAX_VOTE_WEIGHT = reduce(mul, range(1, MAX_VOTE_OPTIONS + 1))
    MSG_REGEX_STR = r'^\!vote((?:\s?\w\d{1,2}){1,%d})' % MAX_VOTE_OPTIONS
    MSG_REGEX = re.compile(MSG_REGEX_STR, re.IGNORECASE)


# TODO: test
def parse_vote(msg: str) -> list[str] | None:
    match = VoteConstants.MSG_REGEX.match(msg)
    if match is None:
        return None

    return match.group(1).split()


def calc_vote_weight(vote_indices: list[int]) -> int:
    assert len(vote_indices) <= VoteConstants.MAX_VOTE_OPTIONS
    return VoteConstants.MAX_VOTE_WEIGHT // len(vote_indices)


# TODO: test
def choose_winners(vote_options: list[VoteOption], max_count: int) -> list[int]:
    enumerated_votes = enumerate(vote_option.votes for vote_option in vote_options)
    sorted_votes = sorted(enumerated_votes, key=lambda x: x[1], reverse=True)
    winners = islice(sorted_votes, max_count)
    winner_indices = [index for index, _ in winners]
    return winner_indices
