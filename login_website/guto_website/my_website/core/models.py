from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class Register(models.Model):
    name = models.CharField(max_length=50, default=None)
    email = models.EmailField()

    is_verified = models.BooleanField(default=False)
    token = models.CharField(max_length = 100, default=None)


class CustomUser(AbstractUser):
    STATUS = (
        ('regular','regular'),
        ('subscriber','subscriber'),
        ('moderator','moderator'),
    )

    email = models.EmailField(unique=True)
    status = models.CharField(max_length=100, choices=STATUS, default='regular')
    description = models.TextField("Descrição", max_length=600, default='', blank=True)
    image = models.ImageField(upload_to='media/', null=True, blank=True)

    def __str__(self):
        return self.username
    

