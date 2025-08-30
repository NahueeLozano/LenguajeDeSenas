from django import forms
from .models import Alumno

class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = ['nombre', 'username', 'contrasena']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre'}),
            'username': forms.TextInput(attrs={'placeholder': 'username'}),
            'contrasena': forms.PasswordInput(attrs={'placeholder': 'Contraseña numérica'}),
        }
