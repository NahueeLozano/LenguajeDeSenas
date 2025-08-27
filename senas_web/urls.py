
from django.contrib import admin
from django.urls import path, include
from senas import views #importamos las vistas de la app
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('senas.urls')  ) , 
    path('senas/login', views.login_view, name='login'),
]
