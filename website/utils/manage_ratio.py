from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait


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

    def set_buy(self, currency, amount):
        if currency:
            self.driver.find_element_by_xpath(f'{self.xpath}/div[5]/div/a').click()
            self.click_on_select(currency, f'{self.xpath}/div[5]/div/div/ul')
            self.buy_currency = currency
        if amount:
            field = self.driver.find_element_by_xpath(f'{self.xpath[:-4] if self.index > 1 else self.xpath}/div[4]/input')
            field.clear()
            field.send_keys(amount)
            self.buy_amount = amount

    def set_sell(self, currency=None, amount=0):
        if currency:
            self.driver.find_element_by_xpath(f'{self.xpath}/div[2]/div/a').click()
            self.click_on_select(currency, f'{self.xpath}/div[2]/div/div/ul')
            self.sell_currency = currency
        if amount:
            field = self.driver.find_element_by_xpath(f'{self.xpath[:-4] if self.index > 1 else self.xpath}/div[3]/input')
            field.clear()
            field.send_keys(amount)
            self.sell_amount = amount

    def delete(self):
        self.driver.find_element_by_xpath(f'{self.xpath[:-4] if self.index > 1 else self.xpath}/div[6]/a').click()


class Manager:
    def __init__(self, league):
        self.driver = webdriver.Chrome()

        self.driver.get('http://currency.poe.trade')
        self.driver.add_cookie({'name': 'apikey', 'value': 'ugahadomaunaba'})

        self.league = league
        self.offer_count = 0
        self.offers = []

        self.go_to_league(self.league)

    def go_to_league(self, league):
        self.driver.get(f'http://currency.poe.trade/shop?league={league}')
        self.offer_count = self.count_offers()
        if self.offer_count > 1:
            self.offer_count += 1
        self.build_offer_list()

    def new_offer(self):
        if self.offer_count > 1:
            self.driver.find_element_by_xpath('//*[@id="content"]/form/div/div/div[6]/div[3]/div[2]/div/a').click()
        offer = Offer(self.driver, self.offer_count)
        self.offers.append(offer)
        self.offer_count += 1
        return offer

    def save(self):
        self.driver.find_element_by_xpath('//*[@id="content"]/form/div/div/div[7]/div/div[2]/input').click()

    def count_offers(self):
        return len(self.driver.find_elements_by_css_selector('.row.offer')) - 1

    def create_new_offer(self, currency_sell, amount_sell, currency_buy, amount_buy):
        offer = self.new_offer()
        offer.set_sell(currency_sell, amount_sell)
        offer.set_buy(currency_buy, amount_buy)

    def build_offer_list(self):
        for index, offer in enumerate(self.driver.find_elements_by_css_selector('.row.offer')[1:]):
            currencies = [string.strip() for string in offer.text.split('\n')]
            self.offers.append(Offer(self.driver, index + 1))
            self.offers[-1].sell_currency = currencies[0]
            self.offers[-1].buy_currency = currencies[1]

    def find_offer(self, sell_currency='', sell_amount=0, buy_currency='', buy_amount=0):
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


manager = Manager('Standard')
# manager.create_new_offer('Chaos Orb', 3, 'Scroll of Wisdom', 50000)
# manager.create_new_offer('Exalted Orb', 3, 'Chaos Orb', 5)
# manager.create_new_offer('Chaos Orb', 3, 'Exalted Orb', 5)
# for offer in reversed(manager.find_offer(sell_currency='')):
#     offer.set_sell(amount=77)
# manager.save()
