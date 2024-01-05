'''Creation of the form to register the user'''
from django.contrib.auth.forms import UserCreationForm
from .models import Register, CustomUser
from django import forms

#Forms
class RegisterForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = ('name','email')
        labels = {
            'name': 'Nome'
        }

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    description = forms.CharField(label="Descrição", widget=forms.Textarea)
    image = forms.ImageField(label="Imagem do Perfil", required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'image','description']


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'description', 'image']