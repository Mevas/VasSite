from django import forms


class RangeInput(forms.widgets.Input):
    input_type = 'range'


class FractionForm(forms.Form):
    numerator = forms.IntegerField(max_value=1000000000, min_value=1)
    denominator = forms.IntegerField(max_value=1000000000, min_value=1)
    first_n = forms.IntegerField(max_value=100, min_value=1)
    precision = forms.IntegerField(max_value=10, min_value=1)
    max_numerator = forms.IntegerField(max_value=1000000000, min_value=1)
    max_denominator = forms.IntegerField(max_value=1000000000, min_value=1)

    def clean(self):
        cleaned_data = super(FractionForm, self).clean()
        numerator = cleaned_data.get('numerator')
        denominator = cleaned_data.get('denominator')
        if not numerator and not denominator:
            raise forms.ValidationError('You have to write something!')

        return cleaned_data
