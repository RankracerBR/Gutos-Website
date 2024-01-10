#Libs/Modules
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


class UserProfileHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    last_name = models.CharField(max_length=100)
    description = models.TextField("Descrição", max_length=600, default='', blank=True)
    image = models.ImageField(upload_to='media/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"History for {self.user.username} at {self.timestamp}"
    

class UserBan(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    is_banned = models.BooleanField(default=False)
    ban_reason = models.TextField("Motivo do Banimento", max_length=500, 
                                  blank=True)
    
    def __str__(self):
        return f"{self.user.username} - Banido: {self.is_banned}"