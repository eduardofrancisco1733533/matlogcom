# Importaciones necesarias
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Ecuacion, Salon
import re  # Módulo para trabajar con expresiones regulares

# Formulario personalizado para la creación de usuarios
class CustomUserCreationForm(UserCreationForm):
    # Se ha agregado un nuevo campo para seleccionar el rol del usuario durante el registro.
    role = forms.ChoiceField(choices=CustomUser.ROLES, required=True, label='Rol', widget=forms.RadioSelect)

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

# Nuevo formulario para añadir ecuaciones. Vinculado al modelo 'Ecuacion'.
class EcuacionForm(forms.ModelForm):
    class Meta:
        model = Ecuacion
        fields = ['ecuacion']

# Nuevo formulario para añadir salones. Vinculado al modelo 'Salon'.
class SalonForm(forms.ModelForm):
    class Meta:
        model = Salon
        fields = ['nombre']

# Formulario para agregar estudiantes a una entidad específica. 
# Utiliza una selección múltiple a través de casillas de verificación.
class AgregarEstudianteForm(forms.Form):
    estudiantes = forms.ModelMultipleChoiceField(queryset=CustomUser.objects.all(), widget=forms.CheckboxSelectMultiple)

# Formulario para la selección de un ícono de perfil. 
# El usuario puede elegir entre varios íconos predefinidos.
class UserProfileForm(forms.ModelForm):
    ICON_CHOICES = [
        ('1.png', 'Icono 1'),
        ('2.png', 'Icono 2'),
        ('3.png', 'Icono 3'),
        # Agrega más opciones para los iconos predefinidos aquí
    ]
    
    profile_icon = forms.ChoiceField(choices=ICON_CHOICES, required=True, label="Selecciona un ícono")

    class Meta:
        model = CustomUser
        fields = ['profile_icon']
