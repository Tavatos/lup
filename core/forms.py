from django import forms
from django.forms.widgets import TextInput

from .models import User_Profile

class ProfilesModelForm(forms.ModelForm):
    class Meta:
        model = User_Profile
        fields = [
        'first_name',
        'last_name',
        'email',
        'address',

    ]