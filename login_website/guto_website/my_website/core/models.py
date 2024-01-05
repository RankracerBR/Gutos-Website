from django.contrib.auth.models import AbstractUser
from simple_history.models import HistoricalRecords
from django.db.models.signals import pre_save
from django.dispatch import receiver
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

    history = HistoricalRecords()

    def __str__(self):
        return self.username


@receiver(pre_save, sender=CustomUser)
def track_user_profile_changes(sender, instance, **kwargs):
    if instance.pk:
        old_user = CustomUser.objects.get(pk=instance.pk)
        if old_user.last_name != instance.last_name or old_user.description != instance.description or old_user.image != instance.image:
            UserProfileHistory.objects.create(
                user=instance,
                last_name=old_user.last_name,
                description=old_user.description,
                image=old_user.image
            )


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