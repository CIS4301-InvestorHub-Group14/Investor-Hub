from django import forms
from django_select2 import forms as s2forms

from .models import SiteUser, Stock


class SignUpForm(forms.ModelForm):
    class Meta:
        model = SiteUser
        fields = ['firstname', 'lastname', 'email', 'dob', 'username', 'password']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'password': forms.PasswordInput()
        }
        labels = {
            'dob': 'Date of Birth'
        }