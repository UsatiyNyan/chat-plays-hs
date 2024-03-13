import pytest

from cph.vote.model import VoteOption
from cph.vote.prepare import (
    VoteConstants,
    parse_vote,
    calc_vote_weight,
    choose_winners,
)


@pytest.mark.parametrize(
    'msg, expected',
    [
        ('!vote a1 B2 c3 D4 e5', ['A1', 'B2', 'C3', 'D4']),
        ('!VotE a1 b2 C3 d4', ['A1', 'B2', 'C3', 'D4']),
        ('!vOte a1 B2 c3', ['A1', 'B2', 'C3']),
        ('!votE h1 m2', ['H1', 'M2']),
        ('!Vote a1', ['A1']),
        ('!vote', None),
        ('wrong', None),
    ]
)
def test_parse_vote(msg, expected):
    assert parse_vote(msg) == expected


@pytest.mark.parametrize(
    'vote_indices, expected',
    [
        ([0, 1, 2, 3, 4], 0),
        ([0, 1, 2, 3], VoteConstants.MAX_VOTE_WEIGHT // 4),
        ([0, 1, 2], VoteConstants.MAX_VOTE_WEIGHT // 3),
        ([0, 1], VoteConstants.MAX_VOTE_WEIGHT // 2),
        ([0], VoteConstants.MAX_VOTE_WEIGHT),
        ([], 0),
    ]
)
def test_calc_vote_weight(vote_indices, expected):
    assert calc_vote_weight(vote_indices) == expected


@pytest.mark.parametrize(
    'vote_options, max_count, expected',
    [
        ([VoteOption('a', 'a1', 1), VoteOption('b', 'b2', 2), VoteOption('c', 'c3', 3)], 1, [2]),  # noqa E501
        ([VoteOption('a', 'a1', 1), VoteOption('b', 'b2', 2), VoteOption('c', 'c3', 3)], 2, [2, 1]),  # noqa E501
        ([VoteOption('a', 'a1', 1), VoteOption('b', 'b2', 2), VoteOption('c', 'c3', 3)], 3, [2, 1, 0]),  # noqa E501
        ([VoteOption('a', 'a1', 1), VoteOption('b', 'b2', 2), VoteOption('c', 'c3', 3)], 4, [2, 1, 0]),  # noqa E501
        ([VoteOption('a', 'a1', 1), VoteOption('b', 'b2', 2), VoteOption('c', 'c3', 3)], 0, []),  # noqa E501
        ([], 1, []),
        ([], 3, []),
    ]
)
def test_choose_winners(vote_options, max_count, expected):
    assert choose_winners(vote_options, max_count) == expected
