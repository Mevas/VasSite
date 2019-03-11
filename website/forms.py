from collections import deque

from django import forms
from website.utils import utils


class FractionForm(forms.Form):
    numerator = forms.IntegerField(min_value=1)
    denominator = forms.IntegerField(min_value=1)
    first_n = forms.IntegerField(min_value=1)
    precision = forms.IntegerField(max_value=10, min_value=0)
    max_numerator = forms.IntegerField(min_value=1)
    max_denominator = forms.IntegerField(min_value=1)

    def clean(self):
        cleaned_data = super(FractionForm, self).clean()
        numerator = cleaned_data.get('numerator')
        denominator = cleaned_data.get('denominator')
        if not numerator and not denominator:
            raise forms.ValidationError('You have to write something!')

        return cleaned_data


class AutoFractionForm(forms.Form):
    choices = [(currency, currency) for currency in utils.get_currency_names()]
    leagues = deque([(league, league) for league in utils.get_trade_league_names()])
    leagues.rotate(2)
    currency_sell = forms.ChoiceField(choices=choices)
    currency_buy = forms.ChoiceField(choices=choices)
    max_numerator = forms.IntegerField(min_value=1)
    max_denominator = forms.IntegerField(min_value=1)
    league = forms.ChoiceField(choices=leagues)
    account_name = forms.CharField()
    api_key = forms.CharField()

    def clean(self):
        cleaned_data = super(AutoFractionForm, self).clean()
        currency_sell = cleaned_data.get('currency_sell')
        currency_buy = cleaned_data.get('currency_buy')
        max_numerator = cleaned_data.get('max_numerator')
        max_denominator = cleaned_data.get('max_denominator')
        league = cleaned_data.get('league')
        account_name = cleaned_data.get('account_name')
        api_key = cleaned_data.get('api_key')

        if not max_numerator and not max_denominator or not league or not currency_buy or not currency_sell or not account_name or not api_key:
            raise forms.ValidationError('You have to write something!')

        return cleaned_data


class ScraperForm(forms.Form):
    name = forms.CharField()
    type = forms.CharField()

    def clean(self):
        cleaned_data = super(ScraperForm, self).clean()
        name = cleaned_data.get('name')

        if not name:
            raise forms.ValidationError('You have to write something!')

        return cleaned_data
