'''Criação do formulário para registro'''
from django import forms
from .models import Registro, PerfilUsuario

class RegistroForm(forms.ModelForm):
    class Meta:
        model = Registro
        fields = ('nome','email')

class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ['image','description']

