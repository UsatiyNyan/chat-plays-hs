from dataclasses import dataclass
from enum import IntEnum, auto

from PySide6.QtCore import (
    Qt,
    QObject,
    QAbstractListModel,
    QModelIndex,
    QPersistentModelIndex,
    QByteArray,
    Property,
    Signal,
)
from PySide6.QtQml import qmlRegisterType

from cph.game.model import GameOption
from cph.vote.model import VoteOption


@dataclass
class VoteElement:
    option: str
    group: str
    alias: str
    votes: int


class VoteModel(QAbstractListModel):
    votesSumChanged = Signal()
    votesMaxChanged = Signal()

    class Roles(IntEnum):
        Option = Qt.ItemDataRole.UserRole
        Group = auto()
        Alias = auto()
        Votes = auto()

    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)
        self._vote_elements: list[VoteElement] = []
        self._votes_sum = 0
        self._votes_max = 0

    def rowCount(self, parent: QModelIndex | QPersistentModelIndex = QModelIndex()) -> int:
        _ = parent
        return len(self._vote_elements)

    def roleNames(self) -> dict[int, QByteArray]:
        return {
            self.Roles.Option: QByteArray(b'option'),
            self.Roles.Group: QByteArray(b'group'),
            self.Roles.Alias: QByteArray(b'alias'),
            self.Roles.Votes: QByteArray(b'votes'),
        }

    def data(self, index: QModelIndex | QPersistentModelIndex, role: int = Qt.ItemDataRole.UserRole) -> str | float | None:
        if index.row() < 0 or index.row() >= self.rowCount():
            return None

        vote_element = self._vote_elements[index.row()]
        match role:
            case self.Roles.Option:
                return vote_element.option
            case self.Roles.Group:
                return vote_element.group
            case self.Roles.Alias:
                return vote_element.alias
            case self.Roles.Votes:
                return vote_element.votes
            case _:
                return None

    @Property(int, notify=votesSumChanged)
    def votesSum(self) -> int:
        return self._votes_sum

    @votesSum.setter
    def votesSum(self, value: int):
        if self._votes_sum == value:
            return
        self._votes_sum = value
        self.votesSumChanged.emit()

    @Property(int, notify=votesMaxChanged)
    def votesMax(self) -> int:
        return self._votes_max

    @votesMax.setter
    def votesMax(self, value: int):
        if self._votes_max != value:
            self._votes_max = value
            self.votesMaxChanged.emit()

    def set_options(self, game_options: list[GameOption], vote_options: list[VoteOption]):
        assert (len(game_options) == len(vote_options))

        def get_option_verified(game_option: GameOption, vote_option: VoteOption):
            assert (game_option.option == vote_option.option)
            return game_option.option

        new_vote_elements = [
            VoteElement(
                option=get_option_verified(game_option, vote_option),
                group=game_option.group,
                alias=vote_option.alias,
                votes=0,
            )
            for game_option, vote_option in zip(game_options, vote_options)
        ]

        self.beginResetModel()
        self._vote_elements = new_vote_elements
        self.endResetModel()

    def update_votes(self, vote_options: list[VoteOption]):
        for vote_element, vote_option in zip(self._vote_elements, vote_options):
            vote_element.votes = vote_option.votes

        if (row_count := self.rowCount()) > 0:
            self.dataChanged.emit(
                self.index(0), self.index(row_count - 1), [self.Roles.Votes])

        self.votesMax = max(vote_option.votes for vote_option in vote_options)
        self.votesSum = sum(vote_option.votes for vote_option in vote_options)


qmlRegisterType(VoteModel, 'Frontend.Bindings', 1, 0, 'VoteModel')
