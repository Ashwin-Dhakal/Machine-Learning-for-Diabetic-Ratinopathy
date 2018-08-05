from django import forms
from .models import All_hostel

class searchform(forms.Form):
    gender= forms.CharField(max_length=100)
    location = forms.CharField(max_length=200)
