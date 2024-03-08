import time
import hslog
import hslog.export
import hslog.packets
import hearthstone.enums
import hearthstone.entities
from pathlib import Path
from cph.game import power_log


def is_card(entity: hearthstone.entities.Entity) -> bool:
    return isinstance(entity, hearthstone.entities.Card)


def is_card_in_hand(entity: hearthstone.entities.Entity) -> bool:
    return is_card(entity) and entity.zone == hearthstone.enums.Zone.HAND


def main():
    power_log_path: Path | None = None
    offset = 0
    parser = hslog.LogParser()

    def read_line(line: str) -> None:
        parser.read_line(line)

    while True:
        power_log_path, offset = \
            power_log.handle_lines_once(read_line, power_log_path, offset)

        print(f'game_meta: {parser.game_meta}')

        for game_pt in parser.games:
            game_pt: hslog.packets.PacketTree
            entity_tree_exporter: hslog.export.EntityTreeExporter = game_pt.export(hslog.export.EntityTreeExporter)
            game = entity_tree_exporter.game
            if game is None:
                continue
            for player in game.players:
                for card in filter(is_card_in_hand, player.entities):
                    print(f'tags: {card.tags}')

        time.sleep(1)


if __name__ == '__main__':
    main()
