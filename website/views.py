from django.http import HttpResponse
from django.shortcuts import render
from website.utils.ratio_calculator import Calculation
from website.utils.tvr_program_scraper import Raport

from .forms import FractionForm, ScraperForm


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
