'''Criação do formulário para registro'''
from django import forms
from .models import Registro

class RegistroForm(forms.ModelForm):
    class Meta:
        model = Registro
        fields = ('nome','email')


