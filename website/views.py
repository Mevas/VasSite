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
    success = True
    account_name = request.COOKIES.get('account_name', '')
    api_key = request.COOKIES.get('api_key', '')

    if request.method == 'POST':
        form = AutoFractionForm(request.POST)
        if form.is_valid():
            form_data = form.clean()

            market_data = get_ratio(form_data['league'], form_data['currency_sell'], form_data['currency_buy'])

            # Initialize cookies if they are not set
            account_name = form_data.get('account_name', account_name)
            api_key = form_data.get('api_key', api_key)

            # Get the next offer if the best one is the user's one or it has less stock
            offer = 0
            while market_data[offer]['account_name'] == account_name or 0 <= market_data[offer]['stock'] < form_data['max_numerator']:
                offer += 1

            undercutting_data = Calculation(market_data[offer]['fraction'].numerator, market_data[offer]['fraction'].denominator, 1, 4, form_data['max_numerator'], form_data['max_denominator']).run()

            manager = Manager(api_key, form_data['league'])
            currencies = utils.get_currency_list()
            url = f'http://currency.poe.trade/search?league={form_data["league"]}&online=x&stock=&want={utils.select_json_element(currencies, form_data["currency_sell"])}&have={utils.select_json_element(currencies, form_data["currency_buy"])}'
            try:
                print(f'Posted {undercutting_data["fractions"][1]["numerator"]} {form_data["currency_sell"]} for {undercutting_data["fractions"][1]["denominator"]} {form_data["currency_buy"]}')
                manager.update_offer(form_data['currency_sell'], undercutting_data['fractions'][1]['numerator'], form_data['currency_buy'], undercutting_data['fractions'][1]['denominator'])
                manager.save()
            except IndexError:
                success = False

            response = render(request, 'website/auto_undercutter.html', {'form': form, 'data': {'success': success, 'url': url}})

            # Set cookies for later uses
            response.set_cookie('account_name', form_data.get('account_name', ''))
            response.set_cookie('api_key', form_data.get('api_key', ''))

            return response
    else:
        form = AutoFractionForm(initial={'account_name': account_name, 'max_numerator': 100, 'max_denominator': 100})
    return render(request, 'website/auto_undercutter.html', {'form': form})


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
