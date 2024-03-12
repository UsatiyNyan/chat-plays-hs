import itertools

from .model import VoteOption


class VoteInterface:
    def set_options(self, vote_options: list[VoteOption], max_count: int):
        self._vote_options = vote_options
        self._max_count = max_count

    def start(self):
        self._connection.start()

    def stop(self) -> list[int]:
        self._connection.stop()

        enumerated_votes = enumerate(vote_option.votes for vote_option in self._vote_options)
        sorted_votes = sorted(enumerated_votes, key=lambda x: x[1], reverse=True)
        winners = itertools.islice(sorted_votes, self._max_count)
        winner_indices = [index for index, _ in winners]
        return winner_indices

    def fetch(self) -> list[VoteOption]:
        # TODO: vote for 1 or vote for 3 options?
        for vote_indices in self._connection.fetch():
            weight = 3 // len(vote_indices)
            for vote_index in vote_indices:
                self._vote_options[vote_index].votes += weight

        return self._vote_options
