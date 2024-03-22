import typing as t
from dataclasses import dataclass

from hearthstone.entities import Entity, Game
from hearthstone.enums import CardType, Zone


@dataclass
class Board:
    ally_hero: int
    hand: list[int]
    ally_minions: list[int]
    enemy_minions: list[int]

    @property
    def free_ally_positions(self) -> t.Iterable[int]:
        ally_minions_size = len(self.ally_minions)
        if ally_minions_size == 7:
            return []
        return range(1, ally_minions_size + 2)

    @classmethod
    def from_game(cls, game: Game) -> 'Board':
        ally = game.current_player
        assert ally is not None

        def is_ally(entity: Entity) -> bool:
            return entity.controller == ally

        def is_minion_or_location(entity: Entity) -> bool:
            return entity.type == CardType.MINION or entity.type == CardType.LOCATION

        hand = filter(is_ally, game.in_zone(Zone.HAND))
        ally_minions = filter(lambda x: is_ally(x) and is_minion_or_location(x),
                              game.in_zone(Zone.PLAY))
        enemy_minions = filter(lambda x: not is_ally(x) and is_minion_or_location(x),
                               game.in_zone(Zone.PLAY))

        return cls(
            ally.hero.id if ally.hero is not None else 0,
            list(card.id for card in hand),
            list(ally.id for ally in ally_minions),
            list(enemy.id for enemy in enemy_minions)
        )
