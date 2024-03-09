import logging
from cph.utils.logging import make_logger
from cph.resources import secrets, hs_api, card_names


def main():
    logger = make_logger('download_card_names', logging.DEBUG)
    secret_keys = secrets.load()
    logger.debug('start downloading')
    downloaded_card_names = hs_api.get_cards(secret_keys.RAPID_API_KEY)
    logger.debug('finish downloading')

    cards: dict[str, str] = {}
    for card_collection_name, card_collection in downloaded_card_names.items():
        logger.debug(f'card collection: {card_collection_name}')
        for card in card_collection:
            cards[card['cardId']] = card['name']

    card_names.save(cards)


if __name__ == '__main__':
    main()
