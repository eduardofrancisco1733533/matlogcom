# Importaciones de Django necesarias para crear modelos y administradores de usuarios personalizados
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# Administrador de usuarios personalizado
class CustomUserManager(BaseUserManager):

    # Método para crear un usuario regular
    def create_user(self, email, username, password=None, **extra_fields):
        # Asegura que se proporciona un correo electrónico
        if not email:
            raise ValueError("El campo Email es necesario")
        # Normaliza el correo (por ejemplo, convierte el dominio a minúsculas)
        email = self.normalize_email(email)
        # Crea una instancia del usuario personalizado
        user = self.model(email=email, username=username, **extra_fields)
        # Asigna y cifra la contraseña
        user.set_password(password)
        # Guarda el usuario en la base de datos
        user.save(using=self._db)
        return user

    # Método para crear un superusuario (administrador)
    def create_superuser(self, email, username, password=None, **extra_fields):
        # Establece que el superusuario tiene privilegios de administrador y de personal
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)

# Modelo de usuario personalizado
class CustomUser(AbstractBaseUser, PermissionsMixin):

    # Opciones de roles que un usuario puede tener
    ROLES = (
        ('STUDENT', 'Estudiante'),
        ('TEACHER', 'Profesor'),
    )
    
    # Campos del modelo de usuario
    email = models.EmailField(unique=True)  # Correo electrónico único para cada usuario
    username = models.CharField(max_length=30, unique=True)  # Nombre de usuario, único para cada usuario
    date_joined = models.DateTimeField(auto_now_add=True)  # Fecha en que se registró el usuario
    is_active = models.BooleanField(default=True)  # Si el usuario está activo en el sistema
    is_staff = models.BooleanField(default=False)  # Si el usuario tiene privilegios de personal
    role = models.CharField(max_length=7, choices=ROLES, null=True, blank=True)  # Rol del usuario (estudiante o profesor)
    profile_icon = models.ImageField(upload_to='media/', null=True, blank=True)  # Icono de perfil del usuario
    points = models.IntegerField(default=0, verbose_name='Puntos')  # Puntos ganados por el usuario en la aplicación
    user_class = models.CharField(max_length=50, default='', blank=True, verbose_name='Clase de usuario')  # Clase a la que pertenece el usuario (no confundir con el modelo `Salon`)

    # Administrador personalizado asignado al modelo
    objects = CustomUserManager()

    # Campo utilizado para identificar al usuario (en este caso, el correo electrónico)
    USERNAME_FIELD = 'email'
    # Otros campos requeridos al crear un usuario
    REQUIRED_FIELDS = ['username']

    # Representación en texto del modelo
    def __str__(self):
        return self.username

# Modelo para almacenar ecuaciones
class Ecuacion(models.Model):
    ecuacion = models.TextField()  # Campo de texto para la ecuación

# Modelo para representar un salón o clase
class Salon(models.Model):
    nombre = models.CharField(max_length=200)  # Nombre del salón o clase
    profesor = models.ForeignKey(CustomUser, related_name='clases_creadas', on_delete=models.CASCADE)  # Profesor que ha creado el salón
    estudiantes = models.ManyToManyField(CustomUser, related_name='clases_asignadas')  # Lista de estudiantes asignados al salón
    ecuacion = models.TextField()  # Ecuación asociada con el salón
