# Importaciones de Django para modelos y administración de usuarios
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# Administrador de usuarios personalizado
class CustomUserManager(BaseUserManager):
    # Método para crear un usuario regular
    def create_user(self, email, username, password=None, **extra_fields):
        # Verificar que el correo electrónico sea proporcionado
        if not email:
            raise ValueError("El campo Email es necesario")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        
        # Asigna un rol por defecto si no se especifica
        user.role = extra_fields.get('role', 'STUDENT')

        user.save(using=self._db)
        return user

    # Método para crear un superusuario
    def create_superuser(self, email, username, password=None, **extra_fields):
        # Establece que el superusuario tiene permisos de administrador y personal
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Establece un rol por defecto para el superusuario
        extra_fields.setdefault('role', 'TEACHER')

        return self.create_user(email, username, password, **extra_fields)

# Modelo de usuario personalizado
class CustomUser(AbstractBaseUser, PermissionsMixin):
    # Opciones de roles para el usuario
    ROLES = (
        ('STUDENT', 'Estudiante'),
        ('TEACHER', 'Profesor'),
    )
    
    # Campos del modelo de usuario
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(max_length=7, choices=ROLES, null=True)
    profile_icon = models.ImageField(upload_to='media/', null=True, blank=True)
    points = models.IntegerField(default=0, verbose_name='Puntos')
    user_class = models.CharField(max_length=50, default='', blank=True, verbose_name='Clase de usuario')

    # Administrador personalizado para el modelo
    objects = CustomUserManager()

    # Campo utilizado como identificador único
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # Representación en cadena del modelo
    def __str__(self):
        return self.username

# Modelo para ecuaciones
class Ecuacion(models.Model):
    ecuacion = models.TextField()
    # Relación con el usuario que crea la ecuación
    profesor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='ecuaciones_creadas', null=True)

    # Representación en cadena del modelo, mostrando un fragmento de la ecuación
    def __str__(self):
        return self.ecuacion[:50] + "..." if len(self.ecuacion) > 50 else self.ecuacion

# Modelo para salones o clases
class Salon(models.Model):
    nombre = models.CharField(max_length=200)
    # Relación con el profesor que crea el salón
    profesor = models.ForeignKey(CustomUser, related_name='clases_creadas', on_delete=models.CASCADE)
    # Relación muchos a muchos con estudiantes asignados al salón
    estudiantes = models.ManyToManyField(CustomUser, related_name='clases_asignadas')

# Modelo para actividades asociadas a salones
class Actividad(models.Model):
    # Relación con el salón al que pertenece la actividad
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE)
    # Relación muchos a muchos con ecuaciones asociadas a la actividad
    ecuaciones = models.ManyToManyField(Ecuacion)
