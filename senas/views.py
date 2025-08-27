import os
import sys
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as login_django
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponse
from .models import Alumno
from .forms import AlumnoForm

# Agrega al PATH de Python la carpeta donde está el script entrenar_modelo.py
# Esto permite importar funciones que están fuera de la carpeta del proyecto Django
sys.path.append(r"C:\Users\w10-21h2\OneDrive\Documentos\ds 2025\programacion\Lengua_de_senas")

# Importa la función main() del archivo entrenar_modelo.py
from entrenar_modelo import main as entrenar_modelo_main

# Vista principal, muestra la página index.html
# Pasa el usuario autenticado a la plantilla
def index(request):
    return render(request, 'senas/index.html', {'usuario': request.user})

# Vista de inicio de sesión
def login_view(request):
    if request.method == 'POST':
        # Obtiene el usuario y contraseña desde el formulario
        username = request.POST.get('username')
        password = request.POST.get('password')
        print("Usuario: ", username)
        print("Contraseña: ", password)

        # Verifica si existe un usuario con esas credenciales
        user = authenticate(username=username, password=password)
        if user:
            # Si existe, inicia sesión
            login_django(request, user)
            return redirect('index')  # Redirige al menú principal
        else:
            # Si las credenciales son inválidas, muestra un error
            return render(request, 'senas/login.html', {'error': 'Credenciales inválidas'})   
        
    # Si el método no es POST, solo muestra el formulario
    return render(request, 'senas/login.html', {})

# Cierra la sesión y redirige al login
def logout_view(request):
    logout(request)
    return redirect('login')

# Vista para entrenar el modelo
@login_required  # Solo usuarios autenticados pueden acceder
def entrenar_modelo(request):
    mensaje = ""
    if request.method == "POST":
        try:
            # Llama a la función que entrena el modelo
            entrenar_modelo_main()
            mensaje = "✅ Entrenamiento completado correctamente."
        except Exception as e:
            mensaje = f"❌ Error durante el entrenamiento: {e}"
    return render(request, 'senas/entrenar.html', {'mensaje': mensaje})

# Página de administración (botones para agregar/listar alumnos)
@login_required
def administracion(request):
    return render(request, 'senas/administracion.html')

# Vista para agregar un alumno usando un formulario
@login_required
def agregar_alumno(request):
    if request.method == 'POST':
        form = AlumnoForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el nuevo alumno en la base de datos
            return redirect('lista_alumnos')
    else:
        form = AlumnoForm()
    return render(request, 'senas/agregar_alumno.html', {'form': form})

# Vista que lista todos los alumnos
@login_required
def lista_alumnos(request):
    alumnos = Alumno.objects.all()  # Obtiene todos los registros de alumnos
    return render(request, 'senas/lista_alumnos.html', {'alumnos': alumnos})

# Elimina un alumno específico por ID
@login_required
def eliminar_alumno(request, alumno_id):
    alumno = get_object_or_404(Alumno, id=alumno_id)  # Si no existe, devuelve 404
    alumno.delete()
    return redirect('lista_alumnos')
