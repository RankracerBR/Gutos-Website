#Libs/Modules
from .models import CustomUser, UserProfileHistory
from django.http import HttpResponse
from django.contrib import admin
import csv


# Register your models here.
#Criar um action para mandar para o RDS da AWS

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