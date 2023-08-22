from django import forms
from django.forms.widgets import TextInput

from .models import Entity
from core.models import User_Profile

class ProfilesModelForm(forms.ModelForm):
    class Meta:
        model = User_Profile
        fields = [
        'username',
        'last_name',
        'email',
        'address',
    ]
        
    
class EntityModelForm(forms.ModelForm):
    class Meta:
        model = Entity
        fields = [
        'entity_name',
        'description',
        'email',
        'address',
        'town',
        'postal_code',
        'province',

    ]