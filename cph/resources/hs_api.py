import requests


HOST = 'omgvamp-hearthstone-v1.p.rapidapi.com'


def get(rapid_api_key: str, route: str):
    headers = {
        'content-type': 'application/octet-stream',
        'X-RapidAPI-Key': rapid_api_key,
        'X-RapidAPI-Host': 'omgvamp-hearthstone-v1.p.rapidapi.com',
    }
    response = requests.get(f'https://{HOST}/{route}', headers=headers)
    if response.status_code != 200:
        raise ConnectionError(response.json())
    return response.json()


def get_cards(rapid_api_key: str):
    return get(rapid_api_key, 'cards')
