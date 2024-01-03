'''Criação do formulário para registro'''
from django.contrib.auth.forms import UserCreationForm
from .models import Register, CustomUser
from django import forms



class RegisterForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = ('name','email')

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    description = forms.CharField(label="Descrição", widget=forms.Textarea)
    image = forms.ImageField(label="Imagem do Perfil", required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'image','description']
