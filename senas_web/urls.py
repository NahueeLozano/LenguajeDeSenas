
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
import os
from senas import views #importamos las vistas de la app
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('senas.urls')  ) , 
    path('senas/login', views.login_view, name='login'),
]
if settings.DEBUG:
    urlpatterns += static('/gifs/', document_root=os.path.join(settings.BASE_DIR, 'gifs'))