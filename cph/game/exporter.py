import typing as t
import logging
from hearthstone import entities, enums
from hslog import packets, player, export, exceptions


class GameStateExporter(export.BaseExporter):
    def __init__(self,
                 manager: player.PlayerManager,
                 logger: logging.Logger):
        super().__init__(packet_tree=None)  # export() is not used
        self.manager = manager
        self.logger = logger
        self.game: entities.Game | None = None

    def _find_entity(self, entity_id: int) -> entities.Entity | None:
        if self.game is None:
            self.logger.warning('find_entity: no game')
            return None
        try:
            return self.game.find_entity_by_id(entity_id)
        except exceptions.MissingPlayerData:
            return None

    def handle_create_game(self, packet: packets.CreateGame):
        self.logger.debug(f'create game: {packet.entity=}')
        self.game = entities.Game(packet.entity)
        self.game.create(packet.tags)
        for player_packet in packet.players:
            self.export_packet(player_packet)

    def handle_player(self, packet: packets.CreateGame.Player):
        if self.game is None:
            self.logger.warning('player: no game')
            return

        entity_id = player.coerce_to_entity_id(packet.entity)
        player_entity = self.manager.get_player_by_entity_id(int(entity_id))
        if player_entity is not None:
            packet.name = player_entity.name
        self.logger.debug(f'player: {entity_id=} name={packet.name}')

        entity = entities.Player(
            entity_id,
            packet.player_id,
            packet.hi,
            packet.lo,
            packet.name
        )
        entity.tags = dict(packet.tags)
        entity.initial_hero_entity_id = entity.tags.get(
            enums.GameTag.HERO_ENTITY, 0)
        self.game.register_entity(entity)

    def handle_block(self, packet: packets.Block):
        if packet.type == enums.BlockType.GAME_RESET and self.game is not None:
            self.logger.debug('game reset')
            self.game.reset()
        super().handle_block(packet)

    def handle_full_entity(self, packet: packets.FullEntity):
        if self.game is None:
            self.logger.warning('full_enitity: no game')
            return

        entity_id = packet.entity
        if self._find_entity(entity_id) is not None:
            self.logger.warning(f'full_entity: {entity_id} already exists')
            return

        entity = entities.Card(int(entity_id), packet.card_id)
        entity.tags = dict(packet.tags)
        self.game.register_entity(entity)

    def handle_hide_entity(self, packet: packets.HideEntity):
        if self.game is None:
            self.logger.warning('hide_entity: no game')
            return
        entity = self._find_entity(packet.entity)
        if entity is None:
            self.logger.warning('hide_entity: entity not found')
            return
        card = t.cast(entities.Card, entity)
        card.hide()

    def handle_show_entity(self, packet: packets.ShowEntity):
        if self.game is None:
            self.logger.warning('show_entity: no game')
            return
        entity = self._find_entity(packet.entity)
        if entity is None:
            self.logger.warning('show_entity: entity not found')
            return
        card = t.cast(entities.Card, entity)
        card.reveal(packet.card_id, dict(packet.tags))

    def handle_change_entity(self, packet: packets.ChangeEntity):
        if self.game is None:
            self.logger.warning('change_entity: no game')
            return
        entity = self._find_entity(packet.entity)
        if entity is None:
            self.logger.warning('change_entity: entity not found')
            return
        card = t.cast(entities.Card, entity)
        if card.card_id is None:
            self.logger.warning(
                'change_entity: '
                f'{packet.entity} to {packet.card_id} with no previous card id')
            return
        card.change(packet.card_id, dict(packet.tags))

    def handle_tag_change(self, packet: packets.TagChange):
        if self.game is None:
            self.logger.warning('tag_change: no game')
            return
        entity_id = player.coerce_to_entity_id(packet.entity)
        entity = self._find_entity(int(entity_id))
        if entity is None:
            self.logger.warning('tag_change: entity not found')
            return
        card = t.cast(entities.Card, entity)
        card.tag_change(packet.tag, packet.value)

    def handle_metadata(self, packet: packets.MetaData):
        pass

    def handle_choices(self, packet: packets.Choices):
        self.logger.debug(f'choices: {packet.player=}')
        for choice in packet.choices:
            entity = self._find_entity(choice)
            self.logger.debug(f'choice: {entity}')
            # TODO: handle COIN <- second player
            # TODO: handle mulligan -> friendly player

    def handle_send_choices(self, packet: packets.SendChoices):
        pass

    def handle_chosen_entities(self, packet: packets.ChosenEntities):
        pass

    def handle_options(self, packet: packets.Options):
        for option in packet.options:
            self.export_packet(option)

    def handle_option(self, packet: packets.Option):
        if self.game is None:
            self.logger.warning('option: no game')
            return

        entity = None if packet.entity is None \
            else self._find_entity(packet.entity)
        self.logger.debug(f'option: {entity} error={packet.error}')

        for target in packet.options:
            target_entity = None if target.entity is None \
                else self._find_entity(target.entity)
            self.logger.debug(f'\ttarget: {target_entity} error={target.error}')

    def handle_send_option(self, packet: packets.SendOption):
        pass

    def handle_reset_game(self, packet: packets.ResetGame):
        pass

    def handle_sub_spell(self, packet: packets.SubSpell):
        super().handle_sub_spell(packet)

    def handle_cached_tag_for_dormant_change(
            self, packet: packets.CachedTagForDormantChange
    ):
        pass

    def handle_vo_spell(self, packet: packets.VOSpell):
        pass

    def handle_shuffle_deck(self, packet: packets.ShuffleDeck):
        pass
