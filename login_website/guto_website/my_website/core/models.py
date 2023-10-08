from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Registro(models.Model):
    nome = models.CharField(max_length=50, default=None)
    email = models.EmailField()

    is_verified = models.BooleanField(default=False)
    token = models.CharField(max_length = 100, default=None)

class CadastroUsuario(models.Model):
    complete_name = models.CharField(max_length=80,default=None)
    complete_email = models.EmailField()
    complete_password = models.CharField(max_length=20, default=None)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.complete_email

    class Meta:
        db_table = 'CadastroUsuario'

class PerfilUsuario(models.Model):
    user = models.OneToOneField(CadastroUsuario, null=True, blank=True, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/')
    description = models.TextField()
