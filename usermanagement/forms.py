from django import forms
from usermanagement.models import *

class LoginForm(forms.Form):
    username = forms.CharField(max_length='30', label='User ID')
    password = forms.CharField(label='Password', widget=forms.TextInput(attrs={'type': 'password'}))

class PrivilegedForm(forms.ModelForm):
    class Meta:
        model = Privileged
        exclude = ('url','created_by_id', 'modified_by_id', 'created_at', 'modified_by',)


