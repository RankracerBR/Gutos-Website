from .models import CadastroUsuario
from django.http import HttpResponse
from django.contrib import admin
import unicodedata
import csv
# Register your models here.

class CadastroUsuarioAdmin(admin.ModelAdmin):
    list_display = ('complete_name', 'complete_email','registration_date','complete_image','complete_description')
    list_filter = ('complete_name','complete_email','registration_date','complete_image')

    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="usuarios.csv"'

        writer = csv.writer(response, delimiter=';')
        writer.writerow(['Nome', 'Email', 'Data de Registro','Descricao']) #Cabeçalhos

        for usuario in queryset:
            normalized_description = unicodedata.normalize('NFKD', usuario.complete_description).encode('ascii','ignore').decode('utf-8')
            writer.writerow([usuario.complete_name, usuario.complete_email, usuario.registration_date, normalized_description])

        return response

    export_to_csv.short_description = "Exportar selecionados para CSV"

    def export_to_sql(self, request, queryset):
        selected_objects = CadastroUsuario.objects.filter(pk__in=queryset.values_list('pk', flat=True))
        
        file_name = "usuarios.sql"

        sql_statements = []
        for obj in selected_objects: #Tirar password
            sql = f"INSERT INTO CadastroUsuario (complete_name, complete_email, complete_image, complete_description, registration_date) VALUES ('{obj.complete_name}', '{obj.complete_email}', '{obj.complete_image}', '{obj.complete_description}', '{obj.registration_date.strftime('%Y-%m-%d %H:%M:%S')}');"
            sql_statements.append(sql)

        sql_content = "\n".join(sql_statements)

        response = HttpResponse(sql_content, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'

        return response

    export_to_sql.short_description = "Exportar selecionados para SQL"

    actions = [export_to_csv, export_to_sql]
     
#Criar um action para mandar para o RDS da AWS

admin.site.register(CadastroUsuario, CadastroUsuarioAdmin)