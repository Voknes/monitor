from django import forms
from .models import Address
import datetime

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address', 'date']
        year = datetime.datetime.now().year

        widgets = {
            'address': forms.TextInput(attrs={'id': 'address', 'class':'form-control form-control-user', 'name': 'address', 'type': 'text', 'placeholder': 'Адрес',}),
            'date': forms.DateInput(attrs={'id': 'date', 'class':'form-control form-control-user', 'name': 'date', 'type': 'date', 'min': '%s-01-01' % (year), 'max': '%s-12-31' % (year), 'placeholder': 'Дата',})
        }