from .models import CustomUser
from django.http import HttpResponse
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
import unicodedata
import csv

# Register your models here.
#Criar um action para mandar para o RDS da AWS

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'status', 'description', 'image')
    list_filter = ('username', 'email', 'status', 'description', 'image')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'description', 'image')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    readonly_fields = ('last_login', 'date_joined')
    
    def display_image(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="50px" height="50px">'
        return 'No Image'

    display_image.allow_tags = True
    display_image.short_description = 'Imagem'

admin.site.register(CustomUser, CustomUserAdmin)
