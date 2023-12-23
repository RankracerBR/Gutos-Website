'''Criação do formulário para registro'''
from django import forms
from .models import Registro, Post, Comment

class RegistroForm(forms.ModelForm):
    class Meta:
        model = Registro
        fields = ('nome','email')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
