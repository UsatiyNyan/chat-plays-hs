import typing as t
import logging
import hearthstone.entities
import hearthstone.enums
import hslog.packets
import hslog.player
import hslog.export
import hslog.exceptions
import hslog.parser


class GameStateExporter(hslog.export.BaseExporter):
    def __init__(self,
                 manager: hslog.player.PlayerManager,
                 logger: logging.Logger):
        super().__init__(packet_tree=None)  # export() is not used
        self.manager = manager
        self.logger = logger
        self.game: hearthstone.entities.Game | None = None

    def _find_entity(self, entity_id: int) -> hearthstone.entities.Entity | None:
        if self.game is None:
            self.logger.warning('find_entity: no game')
            return None
        try:
            return self.game.find_entity_by_id(entity_id)
        except hslog.exceptions.MissingPlayerData:
            return None

    def handle_create_game(self, packet: hslog.packets.CreateGame):
        self.logger.debug(f'create game: {packet.entity=}')
        self.game = hearthstone.entities.Game(packet.entity)
        self.game.create(packet.tags)
        for player_packet in packet.players:
            self.export_packet(player_packet)

    def handle_player(self, packet: hslog.packets.CreateGame.Player):
        if self.game is None:
            self.logger.warning('player: no game')
            return

        entity_id = hslog.player.coerce_to_entity_id(packet.entity)
        player_entity = self.manager.get_player_by_entity_id(int(entity_id))
        if player_entity is not None:
            packet.name = player_entity.name
        self.logger.debug(f'player: {entity_id=} name={packet.name}')

        entity = hearthstone.entities.Player(
            entity_id,
            packet.player_id,
            packet.hi,
            packet.lo,
            packet.name
        )
        entity.tags = dict(packet.tags)
        entity.initial_hero_entity_id = entity.tags.get(
            hearthstone.enums.GameTag.HERO_ENTITY, 0)
        self.game.register_entity(entity)

    def handle_block(self, packet: hslog.packets.Block):
        if packet.type == hearthstone.enums.BlockType.GAME_RESET and self.game is not None:
            self.logger.debug('game reset')
            self.game.reset()
        super().handle_block(packet)

    def handle_full_entity(self, packet: hslog.packets.FullEntity):
        if self.game is None:
            self.logger.warning('full_enitity: no game')
            return

        entity_id = packet.entity
        if self._find_entity(entity_id) is not None:
            self.logger.warning(f'full_entity: {entity_id} already exists')
            return

        entity = hearthstone.entities.Card(int(entity_id), packet.card_id)
        entity.tags = dict(packet.tags)
        self.game.register_entity(entity)

    def handle_hide_entity(self, packet: hslog.packets.HideEntity):
        if self.game is None:
            self.logger.warning('hide_entity: no game')
            return
        entity = self._find_entity(packet.entity)
        if entity is None:
            self.logger.warning('hide_entity: entity not found')
            return
        card = t.cast(hearthstone.entities.Card, entity)
        card.hide()

    def handle_show_entity(self, packet: hslog.packets.ShowEntity):
        if self.game is None:
            self.logger.warning('show_entity: no game')
            return
        entity = self._find_entity(packet.entity)
        if entity is None:
            self.logger.warning('show_entity: entity not found')
            return
        card = t.cast(hearthstone.entities.Card, entity)
        card.reveal(packet.card_id, dict(packet.tags))

    def handle_change_entity(self, packet: hslog.packets.ChangeEntity):
        if self.game is None:
            self.logger.warning('change_entity: no game')
            return
        entity = self._find_entity(packet.entity)
        if entity is None:
            self.logger.warning('change_entity: entity not found')
            return
        card = t.cast(hearthstone.entities.Card, entity)
        if card.card_id is None:
            self.logger.warning(
                'change_entity: '
                f'{packet.entity} to {packet.card_id} with no previous card id')
            return
        card.change(packet.card_id, dict(packet.tags))

    def handle_tag_change(self, packet: hslog.packets.TagChange):
        if self.game is None:
            self.logger.warning('tag_change: no game')
            return
        entity_id = hslog.player.coerce_to_entity_id(packet.entity)
        entity = self._find_entity(int(entity_id))
        if entity is None:
            self.logger.warning('tag_change: entity not found')
            return
        card = t.cast(hearthstone.entities.Card, entity)
        card.tag_change(packet.tag, packet.value)

    def handle_metadata(self, packet: hslog.packets.MetaData):
        pass

    def handle_choices(self, packet: hslog.packets.Choices):
        entity_id = hslog.player.coerce_to_entity_id(packet.entity)
        player_entity = self.manager.get_player_by_entity_id(int(entity_id))
        player_name = player_entity.name if player_entity is not None else None
        first_player = self.manager.first_player
        is_first_player = first_player is not None and first_player.entity_id == entity_id
        self.logger.debug(f'choices: name: {player_name} is first: {is_first_player}')
        for choice in packet.choices:
            entity = self._find_entity(choice)
            self.logger.debug(f'choice: {entity}')
            # TODO: handle COIN <- second player
            # TODO: handle mulligan -> friendly player

    def handle_send_choices(self, packet: hslog.packets.SendChoices):
        pass

    def handle_chosen_entities(self, packet: hslog.packets.ChosenEntities):
        pass

    def handle_options(self, packet: hslog.packets.Options):
        for option in packet.options:
            self.export_packet(option)

    def handle_option(self, packet: hslog.packets.Option):
        if self.game is None:
            self.logger.warning('option: no game')
            return

        entity = None if packet.entity is None \
            else self._find_entity(packet.entity)
        self.logger.debug(f'option: {entity} error={packet.error}')

        for target in packet.options:
            target_entity = None if target.entity is None \
                else self._find_entity(target.entity)
            self.logger.debug(
                f'\ttarget: {target_entity} error={target.error}')

    def handle_send_option(self, packet: hslog.packets.SendOption):
        pass

    def handle_reset_game(self, packet: hslog.packets.ResetGame):
        pass

    def handle_sub_spell(self, packet: hslog.packets.SubSpell):
        super().handle_sub_spell(packet)

    def handle_cached_tag_for_dormant_change(
            self, packet: hslog.packets.CachedTagForDormantChange
    ):
        pass

    def handle_vo_spell(self, packet: hslog.packets.VOSpell):
        pass

    def handle_shuffle_deck(self, packet: hslog.packets.ShuffleDeck):
        pass


def extract_last_game(parser: hslog.LogParser) -> t.Tuple[hslog.packets.PacketTree | None, bool]:
    if len(parser.games) == 0:
        return None, False

    is_new_game = len(parser.games) > 1
    while len(parser.games) > 1:
        parser.games.pop(0)
    return parser.games[0], is_new_game


def handle_packets(parser: hslog.LogParser,
                   logger: logging.Logger,
                   exporter: GameStateExporter | None,
                   packet_offset: int) \
        -> t.Tuple[GameStateExporter | None, int]:
    current_game, is_new_game = extract_last_game(parser)
    if current_game is None:
        return exporter, packet_offset

    exporter = exporter \
        if not is_new_game and exporter is not None\
        else GameStateExporter(parser.player_manager, logger)
    packet_offset = packet_offset if not is_new_game else 0

    for packet in current_game.packets[packet_offset:]:
        exporter.export_packet(packet)
    exporter.flush()

    return exporter, len(current_game.packets)
