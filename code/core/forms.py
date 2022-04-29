
from django import forms
from .models import *

class UserLookupForm(forms.Form):
    class Meta:
        username = forms.CharField()
        fields = ['username']