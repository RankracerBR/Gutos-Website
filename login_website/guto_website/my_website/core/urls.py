#Libs/Modules
from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings
from . import views

#Rotas
urlpatterns = [
    path('', views.Login_Usuario, name='index'), #Rota da pagina principal
    path('send_token/', views.Registration_Token, name="send_token"), #Envio do token
    path('verify/<str:token>', views.verify, name='verify'), #Token 
    path('pagina_usuario/',views.User_Page, name="pagina_usuario"), #Página do usuário 
    path('register_user/', views.CadastroUsuario_1, name="register_user"), #Cadastro no Banco de Dados
    path('atualizar_dados_usuario/', views.Atualizar_Usuario, name="Atualizar_Usuario"), #Atualiza o usuário
    path('logout/', views.Logout_Usuario, name='logout'), #Logout do Usuário
    path('posts/', views.create_post, name="create_post"),
    path('search_images', views.search_images, name="search_images"), # Api de imagens
    re_path(r'^.*/$', views.Login_Usuario, name ='catch_all')#Se o usuário digita algo na url, sempre será redirecionado
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)