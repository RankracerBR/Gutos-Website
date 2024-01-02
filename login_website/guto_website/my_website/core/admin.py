from .models import User
from django.http import HttpResponse
from django.contrib import admin
import unicodedata
import csv

# Register your models here.
#Criar um action para mandar para o RDS da AWS

admin.site.register(User)