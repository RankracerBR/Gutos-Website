'''Criação do formulário para registro'''
from django.contrib.auth.forms import UserCreationForm
from .models import Register, User
from django import forms



class RegisterForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = ('name','email')


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'name', 'password')


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

