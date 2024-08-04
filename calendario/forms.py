from django import forms
from .models import Reserva

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['data']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'})
        }
