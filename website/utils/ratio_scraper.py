from fractions import Fraction

import requests
from bs4 import BeautifulSoup

from website.utils import utils


def get_ratio(league, from_currency, to_currency):
    currencies = utils.get_currency_list()
    url = f'http://currency.poe.trade/search?league={league}&online=x&stock=&want={utils.select_json_element(currencies, from_currency)}&have={utils.select_json_element(currencies, to_currency)}'
    soup = BeautifulSoup(requests.get(url).content, 'lxml')
    ratios = []

    # Gets the ratios from the middle of the row

    for ele in soup.find_all('div', {'class': 'displayoffer'}):
        offer = {'fraction': Fraction(ele['data-sellvalue']) / Fraction(ele['data-buyvalue']), 'stock': ele.get('data-stock', None), 'account_name': ele['data-username']}
        print(offer)
        ratios.append(offer)

    # ratios = sorted({Fraction(ratio[0]) / Fraction(ratio[1]) for ratio in ratios}, reverse=True)

    return ratios
