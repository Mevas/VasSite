from mpmath import mp
import json
import requests


def is_empty(data):
    return data['fractions']


def create_time_string(hours, minutes, seconds, milliseconds, microseconds):
    response = ''

    response = add_time_substring(response, hours, 'hour')
    response = add_time_substring(response, minutes, 'minute')
    response = add_time_substring(response, seconds, 'second')
    response = add_time_substring(response, milliseconds, 'millisecond')
    response = add_time_substring(response, microseconds, 'microsecond')

    return response


def add_time_substring(string, unit, unit_name):
    if unit:
        string += f'{unit} ' + (f'{unit_name}s, ' if unit > 1 else f'{unit_name}, ')

    return string


def humanize_seconds(seconds):
    milliseconds = seconds * 1000 % 1000
    microseconds = round(milliseconds * 1000 % 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    milliseconds = int(milliseconds)
    seconds = int(seconds)
    minutes = int(minutes)
    hours = int(hours)

    response = create_time_string(hours, minutes, seconds, milliseconds, microseconds)

    li = response.rsplit(', ', 2)
    if len(li) > 2:
        response = li[0] + ' and ' + li[1] + ' ' + li[2]
    response = response.rstrip(', ')

    return response


def ratio(fraction):
    return mp.mpf(fraction.numerator) / mp.mpf(fraction.denominator)


def inverse_ratio(fraction):
    return mp.mpf(1) / ratio(fraction)


def get_currency_names():
    import os
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(f'{dir_path}/data/currencies.json') as json_file:
        currencies = json.load(json_file)
        return [currency['name'] for currency in currencies]


def get_league_names():
    url = 'http://api.pathofexile.com/leagues'
    try:
        decoded_json = requests.get(url).json()
        names = [league['id'] for league in decoded_json]
        return names
    except json.decoder.JSONDecodeError:
        return ['Standard', 'Hardcore', 'SSF Standard', 'SSF Hardcore']


def get_trade_league_names():
    return [name for name in get_league_names() if 'SSF' not in name]


def select_json_element(elements, element_to_find):
    for element in elements:
        if element['name'] == element_to_find:
            return element['id']
    return None


def get_currency_name_by_id(id):
    for currency in get_currency_list():
        if currency['id'] == id:
            return currency['name']


def get_currency_list():
    # Local directory needed for some reason
    import os
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(f'{dir_path}/data/currencies.json') as json_file:
        return json.load(json_file)


def get_account_offer_list(account_name):
    # Local directory needed for some reason
    import os
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(f'{dir_path}/data/{account_name}.json') as json_file:
        return json.load(json_file)['offers']


def get_character_names_of_account(account):
    url = f'https://www.pathofexile.com/character-window/get-characters?accountName={account}'
    response = requests.get(url)
    return [character['name'] for character in response.json()]
