# Importaciones necesarias
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# Gestor personalizado para el modelo de usuario
class CustomUserManager(BaseUserManager):
    
    # Método para crear un usuario regular
    def create_user(self, email, username, password=None, **extra_fields):
        # Verifica si se proporcionó un correo electrónico
        if not email:
            raise ValueError("El campo Email es necesario")
        # Normaliza (hace que el dominio del correo sea en minúsculas)
        email = self.normalize_email(email)
        # Crea una instancia de CustomUser
        user = self.model(email=email, username=username, **extra_fields)
        # Asigna y cifra la contraseña
        user.set_password(password)
        # Guarda el usuario en la base de datos
        user.save(using=self._db)
        return user

    # Método para crear un superusuario (admin)
    def create_superuser(self, email, username, password=None, **extra_fields):
        # Establece que el superusuario tiene privilegios de personal y de superusuario
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)

# Modelo personalizado de usuario
class CustomUser(AbstractBaseUser, PermissionsMixin):
    # Define los campos del modelo de usuario
    email = models.EmailField(unique=True)  # Correo electrónico, debe ser único
    username = models.CharField(max_length=30, unique=True)  # Nombre de usuario, debe ser único
    date_joined = models.DateTimeField(auto_now_add=True)  # Fecha en que se unió el usuario
    is_active = models.BooleanField(default=True)  # Si el usuario está activo
    is_staff = models.BooleanField(default=False)  # Si el usuario tiene privilegios de personal

    # Asigna el gestor personalizado al modelo de usuario
    objects = CustomUserManager()

    # Define el campo que se utilizará como identificador de usuario
    USERNAME_FIELD = 'email'
    # Lista de campos que se requerirán al crear un usuario, además del campo definido en USERNAME_FIELD y la contraseña
    REQUIRED_FIELDS = ['username']

    # Método que devuelve una representación en cadena del objeto. En este caso, devuelve el nombre de usuario.
    def __str__(self):
        return self.username

