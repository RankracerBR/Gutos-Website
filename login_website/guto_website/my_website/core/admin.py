#Libs/Modules
from .models import CustomUser, UserProfileHistory, UserBan
from django.http import HttpResponse
from django.contrib import admin
from django.conf import settings
import boto3
import csv
import os


# Register your models here.


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
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


    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="usuarios.csv"'

        writer = csv.writer(response)
        writer.writerow(['Username','Email', 'Status','Description'])

        for user in queryset:
            writer.writerow([
                user.username,
                user.email,
                user.status,
                user.description
            ])
        
        return response
        
    export_to_csv.short_description = 'Exportar para CSV'
    actions = ['export_to_csv']


    def export_to_dynamodb(self, request, queryset):
        aws_access_key_id = settings.AWS_ACCESS_KEY_ID
        aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY
        aws_default_region = settings.AWS_DEFAULT_REGION

        dynamodb = boto3.resource('dynamodb',
                                aws_access_key_id=aws_access_key_id,
                                aws_secret_access_key=aws_secret_access_key,
                                region_name=aws_default_region)
        table = dynamodb.Table('PlatformUsers')

        for user in queryset:
            table.put_item(
                Item={
                    'Partition1': user.username,
                    'email': user.email,
                    'status': user.status,
                    'description': user.description
                }
            )
        self.message_user(request, "Os dados foram enviados para o DynamoDB com sucesso")

    export_to_dynamodb.short_description = "Exportar para o DynamoDB"
    actions = ['export_to_dynamodb']


@admin.register(UserProfileHistory)
class UserProfileHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'description', 'image', 'timestamp')
    list_filter = ('user','description', 'timestamp')


    def has_add_permission(self, request):
        return False

    
    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="usuarios.csv"'

        writer = csv.writer(response)
        writer.writerow(['Username', 'Status','Description'])

        for user in queryset:
            writer.writerow([
                user.user,
                user.email,
                user.status,
                user.description
            ])
        
        return response
        
    export_to_csv.short_description = 'Exportar para CSV'
    actions = ['export_to_csv']


@admin.register(UserBan)
class UserBanAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_banned', 'ban_reason')
    list_filter = ('is_banned',)
    search_fields = ('user__username', 'ban_reason')

    def user_username(self, obj):
        return obj.user.username if obj.user else None
    user_username.short_description = 'Username'
    user_username.admin_order_field = 'user__username'
    