import selenium
from selenium import webdriver


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
    def __init__(self, league):
        # Chrome options for optimal performance in docker
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--window-size=1420,1080')
        chrome_options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)

        self.driver.get('http://currency.poe.trade')
        self.driver.add_cookie({'name': 'apikey', 'value': 'ugahadomaunaba'})

        self.league = league
        self.offer_count = 0
        self.offers = []

        self.go_to_league(self.league)

    def go_to_league(self, league):
        self.driver.get(f'http://currency.poe.trade/shop?league={league}')

        self.offer_count = self.count_offers()
        self.build_offer_list()

        # Increment the offer_count if there is already an offer (stuff breaks without it)
        if self.offer_count > 1 or self.offers and 'Select' not in self.offers[0].sell_currency:
            self.offer_count += 1

    def new_offer(self):
        # If there is 1 offer already, then click on the "new offer" button
        if self.offer_count > 1:
            self.driver.find_element_by_xpath('//*[@id="content"]/form/div/div/div[6]/div[3]/div[2]/div/a').click()

        # Create the offer and append it to the manager master list
        offer = Offer(self.driver, self.offer_count)
        self.offers.append(offer)
        self.offer_count += 1
        return offer

    def save(self):
        self.driver.find_element_by_xpath('//*[@id="content"]/form/div/div/div[7]/div/div[2]/input').click()

    def count_offers(self):
        # Count how many elements have the .row.offer classes, and subtract 1, because there is a hidden template that gets counted
        return len(self.driver.find_elements_by_css_selector('.row.offer')) - 1

    def create_new_offer(self, currency_sell, amount_sell, currency_buy, amount_buy):
        offer = self.new_offer()
        offer.set_sell(currency_sell, amount_sell)
        offer.set_buy(currency_buy, amount_buy)

    def update_offer(self, currency_sell, amount_sell, currency_buy, amount_buy):
        # Check if there is an offer already
        offer = self.find_offer(sell_currency=currency_sell, buy_currency=currency_buy)
        offer = offer[0] if offer else None

        # If not, create a new one and return
        if not offer:
            self.create_new_offer(currency_sell, amount_sell, currency_buy, amount_buy)
            return

        offer.set_sell(amount=amount_sell)
        offer.set_buy(amount=amount_buy)

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
