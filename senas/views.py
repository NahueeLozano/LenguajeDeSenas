import os
import sys
from pathlib import Path
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as login_django
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponse
from .models import Alumno
from .forms import AlumnoForm
from predecir_secuencias import predecir_desde_imagen
import base64
from PIL import Image
from io import BytesIO

# 🔹 Ruta dinámica al archivo entrenar_modelo.py (portátil)
BASE_DIR = Path(__file__).resolve().parents[2]  # Sube dos niveles desde /senas/views.py
sys.path.append(str(BASE_DIR))

# 🔹 Importa la función principal de entrenamiento
from entrenar_modelo import main as entrenar_modelo_main


# -----------------------------
# VISTAS
# -----------------------------

# Vista principal
def index(request):
    return render(request, 'senas/index.html', {'usuario': request.user})


# Vista de inicio de sesión
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login_django(request, user)
            return redirect('index')
        else:
            return render(request, 'senas/login.html', {'error': 'Credenciales inválidas'})   
    return render(request, 'senas/login.html', {})


# Cerrar sesión
def logout_view(request):
    logout(request)
    return redirect('login')


# Vista para entrenar el modelo
@login_required
def entrenar_modelo(request):
    mensaje = ""
    if request.method == "POST":
        try:
            entrenar_modelo_main()
            mensaje = "✅ Entrenamiento completado correctamente."
        except Exception as e:
            mensaje = f"❌ Error durante el entrenamiento: {e}"
    return render(request, 'senas/entrenar.html', {'mensaje': mensaje})


# Vista para predecir señas
def predecir(request):
    mensaje = ""
    resultado = ""
    gif_url = None

    if request.method == "POST":
        imagen_b64 = request.POST.get("imagen")
        if imagen_b64:
            header, data = imagen_b64.split(',', 1)
            imagen_bytes = base64.b64decode(data)
            imagen = Image.open(BytesIO(imagen_bytes))

            # Usa tu función de predicción
            resultado = predecir_desde_imagen(imagen)

            # Buscar GIF asociado
            gif_path = os.path.join("gifs", f"{resultado}.gif")
            if os.path.exists(gif_path):
                gif_url = f"/gifs/{resultado}.gif"
                mensaje = "✅ Seña detectada y GIF mostrado."
            else:
                mensaje = "✅ Seña detectada, pero no hay GIF guardado."
        else:
            mensaje = "❌ No se recibió imagen."

    return render(request, 'senas/predecir.html', {
        'mensaje': mensaje,
        'resultado': resultado,
        'gif_url': gif_url
    })


# Administración
@login_required
def administracion(request):
    return render(request, 'senas/administracion.html')


# Agregar alumno
@login_required
def agregar_alumno(request):
    if request.method == 'POST':
        form = AlumnoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_alumnos')
    else:
        form = AlumnoForm()
    return render(request, 'senas/agregar_alumno.html', {'form': form})


# Listar alumnos
@login_required
def lista_alumnos(request):
    alumnos = Alumno.objects.all()
    return render(request, 'senas/lista_alumnos.html', {'alumnos': alumnos})


# Eliminar alumno
@login_required
def eliminar_alumno(request, alumno_id):
    alumno = get_object_or_404(Alumno, id=alumno_id)
    alumno.delete()
    return redirect('lista_alumnos')
