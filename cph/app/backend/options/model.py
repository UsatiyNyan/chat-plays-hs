from dataclasses import dataclass
from enum import IntEnum, auto

from PySide6.QtCore import (
    Qt,
    QObject,
    QAbstractListModel,
    QModelIndex,
    QPersistentModelIndex,
    QByteArray
)

from cph.utils.math import safe_fraction
from cph.gamestate.model import GameOption
from cph.vote.model import VoteOption


@dataclass
class DisplayOption:
    option: str
    group: str
    alias: str
    vote_fraction: float  # 0.0 to 1.0


class DisplayOptionsModel(QAbstractListModel):
    class Roles(IntEnum):
        Option = Qt.ItemDataRole.UserRole
        Group = auto()
        Alias = auto()
        VoteFraction = auto()

    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)
        self._display_options: list[DisplayOption] = []

    def rowCount(self, parent: QModelIndex | QPersistentModelIndex = QModelIndex()) -> int:
        _ = parent
        return len(self._display_options)

    def roleNames(self) -> dict[int, QByteArray]:
        return {
            self.Roles.Option: QByteArray(b'option'),
            self.Roles.Group: QByteArray(b'group'),
            self.Roles.Alias: QByteArray(b'alias'),
            self.Roles.VoteFraction: QByteArray(b'vote_fraction'),
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
            case self.Roles.VoteFraction:
                return display_option.vote_fraction
            case _:
                return None

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
                vote_fraction=0.0,
            )
            for game_option, vote_option in zip(game_options, vote_options)
        ]

        self.beginResetModel()
        self._display_options = new_display_options
        self.endResetModel()

    def update_votes(self, vote_options: list[VoteOption]):
        votes_max = max(vote_option.votes for vote_option in vote_options)
        for display_option, vote_option in zip(self._display_options, vote_options):
            display_option.vote_fraction = safe_fraction(
                vote_option.votes, votes_max)

        if (row_count := self.rowCount()) > 0:
            self.dataChanged.emit(self.index(0), self.index(
                row_count - 1), [self.Roles.VoteFraction])
