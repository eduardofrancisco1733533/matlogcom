# Importando las herramientas necesarias para definir las rutas URL
from django.urls import path
# Importa las vistas del módulo actual
from . import views

# Lista de rutas URL para la aplicación
urlpatterns = [
    # Cuando se accede a 'registro/', se redirige a la función de vista 'register_view' y tiene un nombre de ruta 'registro'
    path('registro/', views.register_view, name='registro'),
    
    # Ruta para iniciar sesión
    path('login/', views.login_view, name='login'),
    
    # Ruta de bienvenida tras iniciar sesión
    path('bienvenido/', views.bienvenido_view, name='bienvenido'),
    
    # Ruta para cerrar sesión
    path('logout/', views.logout_view, name='logout'),
    
    # Una ruta de prueba, posiblemente para propósitos de desarrollo o para una función específica
    path('prueba/', views.some_view, name='prueba'),
    
    # Una vista relacionada con una funcionalidad de "arrastrar y soltar" (drag and drop)
    path('drag_drop_view/', views.drag_drop_view, name='drag_drop_view'),
    
    # Una vista de bienvenida específica para usuarios invitados
    path('bienvenido_invitado/', views.bienvenido_invitado_view, name='bienvenido_invitado'),
]

