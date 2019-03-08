from django.http import HttpResponse
from django.shortcuts import render
from website.utils.ratio_calculator import Calculation
from website.utils.tvr_program_scraper import Raport
from website.utils.ratio_scraper import get_ratio
from website.utils.manage_ratio import Manager

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
    if request.method == 'POST':
        form = AutoFractionForm(request.POST)
        if form.is_valid():
            form_data = form.clean()
            market_data = get_ratio(form_data['league'], form_data['currency_sell'], form_data['currency_buy'])
            undercutting_data = Calculation(market_data[0].numerator, market_data[0].denominator, 1, 4, form_data['max_numerator'], form_data['max_denominator']).run()
            manager = Manager('Standard')
            try:
                manager.update_offer(form_data['currency_sell'], undercutting_data['fractions'][1]['numerator'], form_data['currency_buy'], undercutting_data['fractions'][1]['denominator'])
                manager.save()
            except IndexError:
                success = False
            return render(request, 'website/auto_undercutter.html', {'form': form})
    else:
        form = AutoFractionForm(initial={'max_numerator': 100, 'max_denominator': 100})
    return render(request, 'website/auto_undercutter.html', {'form': form, 'data': success})


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
