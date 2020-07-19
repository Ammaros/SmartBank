from django import forms
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, User
from .models import Account

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=128, help_text='Input valid email')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('balance',)