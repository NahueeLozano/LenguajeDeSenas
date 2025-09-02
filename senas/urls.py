from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('index/', views.index, name='index'),
    path('logout/', views.logout_view, name='logout'),
    path('entrenar/', views.entrenar_modelo, name='entrenar'),
    path('administracion/', views.administracion, name='administracion'),
    path('agregar-alumno/', views.agregar_alumno, name='agregar_alumno'),
    path('lista_alumnos/', views.lista_alumnos, name='lista_alumnos'),
    path('predecir/', views.predecir, name='predecir'),
    path('eliminar_alumno/<int:alumno_id>/', views.eliminar_alumno, name='eliminar_alumno'),
]
