from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.Login_Usuario, name='index'), #Rota da pagina principal
    path('send_token', views.Registration_Token, name="send_token"), #Envio do token
     path('verify/<str:token>', views.verify, name='verify'), #Token 
    path('pagina_usuario',views.User_page, name="pagina_usuario"), #Página do usuário 
    path('register_user', views.CadastroUsuario_1, name="register_user"), #Cadastro no Banco de Dados
    re_path(r'^.*/$', views.Registration_Token, name = 'catch_all') 
]