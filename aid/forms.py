from django.forms import ModelForm
from django import forms
from .models import *


class AidForm(forms.ModelForm):
    class Meta:
        model = Aid
        fields = ('latitude', 'longitude', 'aid_details')
        widgets = {
            'latitude': forms.TextInput(attrs={'class': 'form-control'}),
            'longitude': forms.TextInput(attrs={'class': 'form-control'}),
            'aid_details': forms.TextInput(attrs={'class': 'form-control'}),
        }
