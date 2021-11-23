from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput, EmailInput

class UserOurReg(UserCreationForm):
    email = forms.EmailField(widget=EmailInput(attrs={'class':'form-control form-control-user', 'placeholder': 'Введите email (необязательно)'}), required=False)
    username = forms.CharField(widget=TextInput(attrs={'class':'form-control form-control-user', 'placeholder': 'Введите логин'}))
    password1 = forms.CharField(widget=PasswordInput(attrs={'class':'form-control form-control-user', 'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(widget=PasswordInput(attrs={'class':'form-control form-control-user', 'placeholder': 'Введите пароль повторно'}))
    name = forms.CharField(widget=TextInput(attrs={'class':'form-control form-control-user', 'placeholder': 'Введите ФИО'}))
    # super_id = forms.HiddenInput()

class UserOurAuth(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class':'form-control form-control-user', 'placeholder': 'Логин'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class':'form-control form-control-user', 'placeholder': 'Пароль'}))