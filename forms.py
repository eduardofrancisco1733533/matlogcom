# Importaciones necesarias
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
import re  # Módulo para trabajar con expresiones regulares

# Formulario personalizado para la creación de usuarios
class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser  # Especifica que este formulario trabaja con el modelo CustomUser
        fields = ('email', 'username')  # Campos que se mostrarán en el formulario

    # Valida el campo email
    def clean_email(self):
        email = self.cleaned_data.get('email')
        allowed_domains = ['outlook.com', 'gmail.com', 'hotmail.com']
        domain = email.split('@')[-1]
        if domain not in allowed_domains:
            raise forms.ValidationError("Solo se permiten emails con dominio outlook.com, gmail.com o hotmail.com.")
        return email

    # Valida el campo de contraseña
    def clean_password1(self):
        password = self.cleaned_data.get('password1')

        # Las siguientes condiciones aseguran que la contraseña cumpla con ciertos criterios
        if len(password) < 6:
            raise forms.ValidationError("La contraseña debe tener al menos 6 caracteres.")
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError("La contraseña debe contener al menos una letra mayúscula.")
        if len(re.findall(r'[0-9]', password)) < 2:
            raise forms.ValidationError("La contraseña debe contener al menos dos números.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise forms.ValidationError("La contraseña debe contener al menos un carácter especial.")

        return password

# Formulario personalizado para cambiar los detalles de los usuarios
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser  # Especifica que este formulario trabaja con el modelo CustomUser
        fields = ('email', 'username')  # Campos que se mostrarán en el formulario


