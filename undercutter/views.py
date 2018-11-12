from django.shortcuts import render
from undercutter.utils.ratio_calculator import Calculation

from .forms import FractionForm


def index(request):
    return render(request, 'undercuttrer/homepage.html')


def undercutter(request):
    if request.method == 'POST':
        form = FractionForm(request.POST)
        if form.is_valid():
            form_data = form.clean()
            data = Calculation(form_data['numerator'], form_data['denominator'], form_data['first_n'], form_data['precision'], form_data['max_numerator'], form_data['max_denominator']).run()
            return render(request, 'undercuttrer/undercutter.html', {'form': form, 'data': data})
    else:
        form = FractionForm(initial={'first_n': 10, 'precision': 4, 'max_numerator': 100, 'max_denominator': 100})
        print(form)

    return render(request, 'undercuttrer/undercutter.html', {'form': form})
