from django.http import HttpResponse
from django.shortcuts import render
from website.utils.ratio_calculator import Calculation
from website.utils.tvr_program_scraper import Raport
from website.utils.ratio_scraper import get_ratio
from website.utils.manage_ratio import Manager
from website.utils import utils

from .forms import FractionForm, AutoFractionForm, ScraperForm


def index(request):
    return render(request, 'website/homepage.html')


def undercutter(request):
    if request.method == 'POST':
        form = FractionForm(request.POST)
        if form.is_valid():
            form_data = form.clean()
            data = Calculation(form_data['numerator'], form_data['denominator'], form_data['first_n'], form_data['precision'], form_data['max_numerator'], form_data['max_denominator']).run()
            return render(request, 'website/undercutter.html', {'form': form, 'data': data})
    else:
        form = FractionForm(initial={'first_n': 10, 'precision': 4, 'max_numerator': 100, 'max_denominator': 100})

    return render(request, 'website/undercutter.html', {'form': form})


def auto_undercutter(request):
    account_name = request.COOKIES.get('account_name', '')
    api_key = request.COOKIES.get('api_key', '')
    offers = [{**offer, 'league': 'Synthesis'} for offer in utils.get_account_offer_list(account_name)['Synthesis']]

    if request.method == 'POST':
        form = AutoFractionForm(request.POST)
        if form.is_valid():
            form_data = form.clean()

            # Initialize cookies if they are not set
            account_name = form_data.get('account_name', account_name)
            api_key = form_data.get('api_key', api_key)
            form_league = form_data.get('league', 'Standard')

            manager = Manager(api_key, form_data['league'])

            if 'update-one' in request.POST:
                success, url = update_offer(manager, account_name, form_data)
            else:
                for sell in range(1, 16 + 1):
                    for buy in range(1, 16 + 1):
                        if sell in [3, 6] or buy in [6] or sell == buy or sell in [] or buy == 3 and sell == 8 or sell == 3 and buy == 8:
                            continue
                        # [2, 3, 6, 7, 11, 14]
                        sell_max = 20 if sell in [2, 3, 10] else 100
                        if sell in [5, 11, 13, 14, 16]:
                            sell_max = 10
                        if sell in [6, 15]:
                            sell_max = 1
                        buy_max = 20 if buy in [2, 3, 10] else 100
                        if buy in [4, 5, 11, 13, 14, 16]:
                            buy_max = 10
                        if buy in [6, 15]:
                            buy_max = 1
                        if buy in [3]:
                            sell_max = 2000
                        if sell == 4:
                            sell_max = 5
                        if sell == 4 and buy not in []:
                            continue
                        if buy == 4 and sell not in []:
                            continue
                        if buy == 3 and sell not in [8]:
                            continue

                        data = {'league': form_league, 'currency_sell': sell, 'max_numerator': sell_max, 'currency_buy': buy, 'max_denominator': buy_max}
                        success, url = update_offer(manager, account_name, data)
                        if not success:
                            print(f'Failed at {sell} -> {buy}')
                        else:
                            print(url, sell, buy)
                # success = True
                # for league, offer_list in utils.get_account_offer_list(account_name).items():
                #     for offer in offer_list:
                #         if not offer['active']:
                #             continue
                #
                #         data = {'league': league, 'currency_sell': offer['sell_id'], 'max_numerator': offer['sell_max'], 'currency_buy': offer['buy_id'], 'max_denominator': offer['buy_max']}
                #         success, url = update_offer(manager, account_name, data)
                #         if not success:
                #             print(f'Failed at {offer}')
                #         else:
                #             print(url, offer['buy_id'], offer['sell_id'])

            manager.save()

            response = render(request, 'website/auto_undercutter.html', {'form': form, 'data': {'success': success, 'url': url}})

            # Set cookies for later uses
            response.set_cookie('account_name', account_name)
            response.set_cookie('api_key', api_key)

            return response
    else:
        form = AutoFractionForm(initial={'max_numerator': 100, 'max_denominator': 100, 'account_name': account_name, 'api_key': api_key})
    return render(request, 'website/auto_undercutter.html', {'form': form, 'data': {'offers': offers}})


def update_offer(manager, account_name, data):
    if isinstance(data['currency_sell'], int):
        data['currency_sell'] = utils.get_currency_name_by_id(data['currency_sell'])
    if isinstance(data['currency_buy'], int):
        data['currency_buy'] = utils.get_currency_name_by_id(data['currency_buy'])

    print(f"Updating offer of account {account_name}: {data['currency_sell']} -> {data['currency_buy']} in {data['league']} league")

    success = True
    currencies = utils.get_currency_list()

    market_data = get_ratio(data['league'], data['currency_sell'], data['currency_buy'])

    if len(market_data) == 0:
        return False, ''

    # Get the next offer if the best one is the user's one or it has less stock
    offer = 0
    while offer < len(market_data) - 1 and ((market_data[offer]['account_name'] == account_name or 0 <= market_data[offer]['stock'] < data['max_numerator'] or market_data[offer]['fraction'] / market_data[offer+1]['fraction'] >= 1.2 or 0 <= market_data[offer]['stock'] <= market_data[offer]['fraction'].numerator) and not market_data[offer]['stock'] > market_data[offer]['fraction'].numerator):
        offer += 1

    undercutting_data = Calculation(market_data[offer]['fraction'].numerator, market_data[offer]['fraction'].denominator, 1, 4, data['max_numerator'], data['max_denominator']).run()

    url = f'http://currency.poe.trade/search?league={data["league"]}&online=x&stock=&want={utils.select_json_element(currencies, data["currency_sell"])}&have={utils.select_json_element(currencies, data["currency_buy"])}'
    try:
        manager.change_offer(data['currency_sell'], undercutting_data['fractions'][1]['numerator'], data['currency_buy'], undercutting_data['fractions'][1]['denominator'])
    except IndexError:
        success = False

    if success:
        print(f'Posted {undercutting_data["fractions"][1]["numerator"]} {data["currency_sell"]} -> {undercutting_data["fractions"][1]["denominator"]} {data["currency_buy"]}')
    else:
        print('Error - updating failed')

    return success, url


def program_scraper(request):
    if request.method == 'POST':
        form = ScraperForm(request.POST)
        if form.is_valid():
            form_data = form.clean()
            raport = Raport(form_data['name'], form_data['type']).run()

            response = HttpResponse(raport['data'], content_type='application/ms-excel')
            response['Content-Disposition'] = f'attachment; filename="{raport["filename"]}"'
            return response
            # return render(request, 'website/undercutter.html', {'form': form})
    else:
        form = ScraperForm(initial={'type': 'Cameraman'})

    return render(request, 'website/program_scraper.html', {'form': form})
