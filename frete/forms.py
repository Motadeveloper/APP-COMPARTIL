# frete/forms.py
from django import forms

class EnderecoForm(forms.Form):
    cep = forms.CharField(label='CEP', max_length=10)
    frete = forms.DecimalField(label='Frete', max_digits=10, decimal_places=2, required=False, widget=forms.HiddenInput())
