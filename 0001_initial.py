from django.db import migrations, models

class Migration(migrations.Migration):

    # Indica si esta es la primera migración para esta aplicación.
    initial = True

    # Lista de otras migraciones en las que esta migración depende.
    # Aquí, depende de una migración específica en la aplicación 'auth'.
    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    # Lista de operaciones a realizar. Estas alterarán la estructura de la base de datos.
    operations = [
        # Se crea un nuevo modelo llamado 'Ecuacion'.
        migrations.CreateModel(
            name='Ecuacion',
            fields=[
                # ID es un campo de autoincremento utilizado como clave primaria.
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                # Campo de texto para almacenar ecuaciones matemáticas o fórmulas.
                ('ecuacion', models.TextField()),
            ],
        ),
        # Se crea un nuevo modelo llamado 'CustomUser'.
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                # ID es un campo de autoincremento utilizado como clave primaria.
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                # Campo de contraseña para el usuario.
                ('password', models.CharField(max_length=128, verbose_name='password')),
                # Fecha y hora del último inicio de sesión del usuario.
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                # Booleano que indica si el usuario es un superusuario.
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                # Dirección de correo electrónico del usuario.
                ('email', models.EmailField(max_length=254, unique=True)),
                # Nombre de usuario.
                ('username', models.CharField(max_length=30, unique=True)),
                # Fecha y hora en que se unió el usuario.
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                # Booleano que indica si el usuario está activo.
                ('is_active', models.BooleanField(default=True)),
                # Booleano que indica si el usuario es parte del personal.
                ('is_staff', models.BooleanField(default=False)),
                # Imagen o ícono de perfil para el usuario. Se almacenará en el directorio 'media/'.
                ('profile_icon', models.ImageField(blank=True, null=True, upload_to='media/')),
                # Campo que representa un sistema de puntos para el usuario.
                ('points', models.IntegerField(default=0, verbose_name='Puntos')),
                # Campo para categorizar o nivelar a los usuarios (e.g., "Novato", "Experto").
                ('user_class', models.CharField(blank=True, default='', max_length=50, verbose_name='Clase de usuario')),
                # Relación muchos a muchos con grupos que el usuario pertenece.
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                # Relación muchos a muchos con permisos específicos para este usuario.
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            # Opciones adicionales para el modelo.
            options={
                'abstract': False,
            },
        ),
    ]