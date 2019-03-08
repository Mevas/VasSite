import re
from fractions import Fraction

from bs4 import BeautifulSoup
import requests
import json


def select_json_element(elements, element_to_find):
    for element in elements:
        if element['name'] == element_to_find:
            return element['id']
    return None


def get_ratio(league, from_currency, to_currency):
    # Local directory needed for some reason
    import os
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(f'{dir_path}/data/currencies.json') as json_file:
        currencies = json.load(json_file)

    url = f'http://currency.poe.trade/search?league={league}&online=x&stock=&want={select_json_element(currencies, from_currency)}&have={select_json_element(currencies, to_currency)}'
    soup = BeautifulSoup(requests.get(url).content, 'lxml')
    ratios = []

    print(url)

    # Gets the ratios from the middle of the row
    # TODO: Get stock information
    for ele in soup.find_all('div', {'class': 'displayoffer-middle'}):
        ratios.append([float(s) for s in re.findall(r'-?\d+\.?\d*', ele.text)])
    ratios = sorted({Fraction(ratio[0]) / Fraction(ratio[1]) for ratio in ratios}, reverse=True)

    return ratios
