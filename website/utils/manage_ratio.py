import urllib

import requests
import selenium

from website.utils import utils


class Offer:
    def __init__(self, driver, index):
        self.driver = driver
        self.index = index
        self.xpath = f'//*[@id="offers"]/div[{self.index}]'

        if self.index > 1:
            self.xpath += '/div'

        self.buy_currency = 0
        self.buy_amount = 0
        self.sell_currency = 0
        self.sell_amount = 0

    def click_on_select(self, text, xpath):
        select = self.driver.find_element_by_xpath(xpath)
        for option in select.find_elements_by_class_name('active-result'):
            if option.text == text:
                option.click()  # select() in earlier versions of webdriver
                break

    def set_buy(self, currency=None, amount=0):
        if currency:
            self.driver.find_element_by_xpath(f'{self.xpath}/div[5]/div/a').click()
            self.click_on_select(currency, f'{self.xpath}/div[5]/div/div/ul')
            self.buy_currency = currency
        if amount:
            try:
                field = self.driver.find_element_by_xpath(f'{self.xpath}/div[4]/input')
            except selenium.common.exceptions.NoSuchElementException:
                field = self.driver.find_element_by_xpath(f'{self.xpath[:-4]}/div[4]/input')
            field.clear()
            field.send_keys(amount)
            self.buy_amount = amount

    def set_sell(self, currency=None, amount=0):
        if currency:
            self.driver.find_element_by_xpath(f'{self.xpath}/div[2]/div/a').click()
            self.click_on_select(currency, f'{self.xpath}/div[2]/div/div/ul')
            self.sell_currency = currency
        if amount:
            try:
                field = self.driver.find_element_by_xpath(f'{self.xpath}/div[3]/input')
            except selenium.common.exceptions.NoSuchElementException:
                field = self.driver.find_element_by_xpath(f'{self.xpath[:-4]}/div[3]/input')
            field.clear()
            field.send_keys(amount)
            self.sell_amount = amount

    def delete(self):
        self.driver.find_element_by_xpath(f'{self.xpath[:-4] if self.index > 1 else self.xpath}/div[6]/a').click()


class Manager:
    def __init__(self, api_key, league=''):
        # Chrome options for optimal performance in docker
        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--no-sandbox')
        # # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--window-size=1420,2060')
        # chrome_options.add_argument('--disable-gpu')
        # self.driver = webdriver.Chrome(options=chrome_options)
        # self.driver.implicitly_wait(10)
        #
        # self.driver.get('http://currency.poe.trade')
        # self.driver.add_cookie({'name': 'apikey', 'value': api_key})

        # Set the default league to the softcore temporary league if one is not specifed
        self.leagues = utils.get_trade_league_names()
        self.league = league if league else self.leagues[2] if len(self.leagues) > 2 else 'Standard'
        self.api_key = api_key

        self.offer_count = 0
        self.offers = []

        self.offer_string = f'league={self.league}&apikey={self.api_key}'

        # self.go_to_league(self.league)

    def save(self):
        url = f'http://currency.poe.trade/shop?league={self.league}'
        self.offer_string = urllib.parse.quote_plus(self.offer_string, safe='/&=')

        requests.post(url, data=self.offer_string, headers={'Content-Type': 'application/x-www-form-urlencoded'})

    def count_offers(self):
        # Count how many elements have the .row.offer classes, and subtract 1, because there is a hidden template that gets counted
        return len(self.driver.find_elements_by_css_selector('.row.offer')) - 1

    def change_offer(self, currency_sell, amount_sell, currency_buy, amount_buy):
        url = f'http://currency.poe.trade/shop?league={self.league}'
        self.offer_string += f'&sell_currency={currency_sell}&sell_value={amount_sell}&buy_value={amount_buy}&buy_currency={currency_buy}'

        requests.post(url, data={'league': self.league, 'apikey': self.api_key, 'sell_currency': currency_sell, 'sell_value': amount_sell, 'buy_currency': currency_buy, 'buy_value': amount_buy})

    def build_offer_list(self):
        for index, offer in enumerate(self.driver.find_elements_by_css_selector('.row.offer')[1:]):
            currencies = [string.strip() for string in offer.text.split('\n')]
            self.offers.append(Offer(self.driver, index + 1))
            self.offers[-1].sell_currency = currencies[0]
            self.offers[-1].buy_currency = currencies[1]

    def find_offer(self, sell_currency='', sell_amount=0, buy_currency='', buy_amount=0):
        # Finds an offer based on an AND gate
        offers = []

        for offer in self.offers:
            found = True

            if sell_currency and offer.sell_currency != sell_currency:
                found = False
            if sell_amount and offer.sell_amount != sell_amount:
                found = False
            if buy_currency and offer.buy_currency != buy_currency:
                found = False
            if buy_amount and offer.buy_amount != buy_amount:
                found = False

            if found:
                offers.append(offer)

        return offers
