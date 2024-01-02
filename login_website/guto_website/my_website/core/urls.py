#Libs/Modules
from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings
#from . import views

#Rotas
urlpatterns = [


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)