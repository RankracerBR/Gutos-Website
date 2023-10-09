from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.Login_Usuario, name='index'), #Rota da pagina principal
    path('send_token', views.Registration_Token, name="send_token"), #Envio do token
    path('verify/<str:token>', views.verify, name='verify'), #Token 
    path('pagina_usuario',views.User_Page, name="pagina_usuario"), #Página do usuário 
    path('register_user', views.CadastroUsuario_1, name="register_user"), #Cadastro no Banco de Dados
    re_path(r'^.*/$', views.Registration_Token, name = 'catch_all') 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)