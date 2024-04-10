from django import forms
from .models import SiteUser


class SignUpForm(forms.ModelForm):
    class Meta:
        model = SiteUser
        fields = ['firstname', 'lastname', 'email', 'dob', 'username', 'password']