from .models import CadastroUsuario, PerfilUsuario
from django.http import HttpResponse
from django.contrib import admin
import csv
# Register your models here.

class CadastroUsuarioAdmin(admin.ModelAdmin):
    list_display = ('complete_name', 'complete_email','registration_date')
    list_filter = ('complete_name','complete_email','registration_date')


    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="usuarios.csv"'

        writer = csv.writer(response, delimiter=';')
        writer.writerow(['Nome', 'Email', 'Data de Registro']) #Cabeçalhos

        for usuario in queryset:
            writer.writerow([usuario.complete_name, usuario.complete_email, usuario.registration_date])

        return response

    export_to_csv.short_description = "Exportar selecionados para CSV"

    actions = [export_to_csv]

class PerfiUsuarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'image', 'description')

admin.site.register(PerfilUsuario, PerfiUsuarioAdmin)
admin.site.register(CadastroUsuario, CadastroUsuarioAdmin)