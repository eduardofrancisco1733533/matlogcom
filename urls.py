# Importando las herramientas necesarias para definir las rutas URL
from django.urls import path
# Importa las vistas del módulo actual
from . import views
# Importa las herramientas para configuración y gestión de URLs estáticas
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Ruta para la página de registro de usuarios
    path('registro/', views.register_view, name='registro'),

    # Ruta para la página de inicio de sesión
    path('login/', views.login_view, name='login'),

    # Ruta para la página de bienvenida tras iniciar sesión
    path('bienvenido/', views.bienvenido_view, name='bienvenido'),

    # Ruta para la página de perfil de usuario
    path('perfil/', views.profile_view, name='profile'),

    # Ruta para cerrar sesión
    path('logout/', views.logout_view, name='logout'),

    # Ruta para una página de prueba
    path('prueba/', views.some_view, name='prueba'),

    # Ruta para una funcionalidad de arrastrar y soltar
    path('drag_drop_view/', views.drag_drop_view, name='drag_drop_view'),

    # Ruta para una página de bienvenida específica para usuarios invitados
    path('bienvenido_invitado/', views.bienvenido_invitado_view, name='bienvenido_invitado'),

    # Ruta que permite a los usuarios ingresar ecuaciones
    path('ingresar/', views.ingresar_ecuacion, name='ingresar_ecuacion'),

    # Ruta para crear una nueva ecuación
    path('crearEcuacion/', views.crear_ecuacion, name='crear_ecuacion'),

    # Ruta para crear un nuevo salón o clase
    path('crear/', views.crear_salon, name='crear_salon'),

    # Ruta para agregar estudiantes a un salón específico
    path('agregar_estudiante/<int:salon_id>/', views.agregar_estudiante, name='agregar_estudiante'),

    # Ruta para ver todos los salones o clases a los que pertenece el usuario
    path('misClases/', views.mis_salones, name='mis_salones'),

    # Ruta para ver detalles de un salón o clase específico
    path('detalleSalon/<int:salon_id>/', views.detalle_salon, name='detalle_salon'),
]

# Si estamos en modo de desarrollo (DEBUG = True), se configuran las URLs para servir archivos multimedia
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

