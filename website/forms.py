from django import forms


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


class ScraperForm(forms.Form):
    name = forms.CharField()
    type = forms.CharField()

    def clean(self):
        cleaned_data = super(ScraperForm, self).clean()
        name = cleaned_data.get('name')

        if not name:
            raise forms.ValidationError('You have to write something!')

        return cleaned_data
