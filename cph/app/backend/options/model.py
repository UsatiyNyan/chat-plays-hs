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

from cph.gamestate.model import GameOption
from cph.vote.model import VoteOption


@dataclass
class DisplayOption:
    option: str
    group: str
    alias: str
    votes: int


class DisplayOptionsModel(QAbstractListModel):
    votesSumChanged = Signal()
    votesMaxChanged = Signal()

    class Roles(IntEnum):
        Option = Qt.ItemDataRole.UserRole
        Group = auto()
        Alias = auto()
        Votes = auto()

    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)
        self._display_options: list[DisplayOption] = []
        self._votes_sum = 0
        self._votes_max = 0

    def rowCount(self, parent: QModelIndex | QPersistentModelIndex = QModelIndex()) -> int:
        _ = parent
        return len(self._display_options)

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

        display_option = self._display_options[index.row()]
        match role:
            case self.Roles.Option:
                return display_option.option
            case self.Roles.Group:
                return display_option.group
            case self.Roles.Alias:
                return display_option.alias
            case self.Roles.Votes:
                return display_option.votes
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
        if self._votes_max == value:
            return
        self._votes_max = value
        self.votesMaxChanged.emit()

    def set_options(self, game_options: list[GameOption], vote_options: list[VoteOption]):
        assert (len(game_options) == len(vote_options))

        def get_option_verified(game_option: GameOption, vote_option: VoteOption):
            assert (game_option.option == vote_option.option)
            return game_option.option

        new_display_options = [
            DisplayOption(
                option=get_option_verified(game_option, vote_option),
                group=game_option.group,
                alias=vote_option.alias,
                votes=0,
            )
            for game_option, vote_option in zip(game_options, vote_options)
        ]

        self.beginResetModel()
        self._display_options = new_display_options
        self.endResetModel()

    def update_votes(self, vote_options: list[VoteOption]):
        for display_option, vote_option in zip(self._display_options, vote_options):
            display_option.votes = vote_option.votes

        if (row_count := self.rowCount()) > 0:
            self.dataChanged.emit(
                self.index(0), self.index(row_count - 1), [self.Roles.Votes])

        self.votesMax = max(vote_option.votes for vote_option in vote_options)
        self.votesSum = sum(vote_option.votes for vote_option in vote_options)


qmlRegisterType(DisplayOptionsModel, 'Frontend.Bindings', 1, 0, 'VoteModel')
