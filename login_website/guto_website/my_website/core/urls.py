#Libs/Modules
from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings
from . import views

#Rotas
urlpatterns = [
path('', views.Login_user, name='index'),
path('send_token/', views.Registration_Token, name="send_token"), #Envio do token
path('verify/<str:token>', views.Verify, name='verify'), #Token 
path('registrar_conta/', views.Register_user, name='register_account'),
path('pagina_usuario/', views.User_page, name='user_page')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)