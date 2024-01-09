#Libs/Modules
from django.views.decorators.csrf import csrf_exempt
from django_ratelimit.decorators import ratelimit
from django.conf.urls.static import static
from django.urls import path, re_path
from django.conf import settings
from . import views

#Routes
urlpatterns = [
    path('', views.Login_user, name='index'),
    path('send_token/', csrf_exempt(ratelimit(key='ip', rate='5/m')(views.Registration_Token)), name='send_token'),
    path('verify/<str:token>', views.Verify, name='verify'),
    path('registrar_conta/', csrf_exempt(ratelimit(key='ip', rate='5/m')(views.Register_user)), name='register_account'),
    path('pagina_usuario/', views.User_page, name='user_page'),
    path('update_user/', views.Update_user, name="update_user"),
    path('logout', views.Logout_user, name="logout"),
    path('pesquisa_imagens', views.Search_images, name='search_images'),
    path('usuarios/', views.Users, name='show_users'),
    re_path(r'^\d+/$', views.Login_user, name='catch_all')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)