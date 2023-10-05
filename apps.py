# Importa la clase base AppConfig desde django.apps
from django.apps import AppConfig

# Define una subclase de AppConfig para la app 'cuentas'
class CuentasConfig(AppConfig):
    # Define el tipo de campo a utilizar por defecto para la generación automática de IDs
    # cuando no se especifica un campo primary key explícitamente en un modelo.
    default_auto_field = 'django.db.models.BigAutoField'
    
    # El nombre canónico de la aplicación, es decir, el nombre utilizado en las importaciones y referencias.
    name = 'cuentas'
