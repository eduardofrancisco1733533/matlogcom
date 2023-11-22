from django.db.models import F
import random
from django.http import HttpResponseForbidden, HttpResponseNotFound, JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import CustomUser, ProgresoActividad
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from cuentas.models import Actividad, Ecuacion, Salon, IntentoEcuacion 
from .forms import (
    ActividadForm,
    AgregarEstudianteForm,
    CustomUserCreationForm,
    EcuacionForm,
    SalonForm,
    UserProfileForm,
)
from django.contrib import messages
from sympy import SympifyError, symbols, Eq, solve, sympify
import re
from fractions import Fraction
from sympy import Rational

# Función para comparar respuestas con soluciones de ecuaciones
# Evalúa si la respuesta del estudiante es aproximadamente igual a la solución de Sympy.
def comparar_respuestas(respuesta_estudiante, solucion_sympy, tolerancia=0.01):
    try:
        # Intenta convertir ambas respuestas a formato decimal y las compara dentro de un margen de tolerancia.
        respuesta_decimal = float(respuesta_estudiante)
        solucion_decimal = float(solucion_sympy.evalf())
        return abs(respuesta_decimal - solucion_decimal) < tolerancia
    except ValueError:
        # Si la conversión a decimal falla, intenta convertir a fracciones.
        try:
            respuesta_fraccion = Fraction(respuesta_estudiante)
            if isinstance(solucion_sympy, Rational):
                solucion_fraccion = Fraction(solucion_sympy.p, solucion_sympy.q)
                return respuesta_fraccion == solucion_fraccion
            return False
        except ValueError:
            # Si no se pueden convertir a fracciones, la respuesta se considera incorrecta.
            return False

# Decorador para restringir el acceso a las vistas solo a usuarios con rol de "Profesor"
def teacher_required(view_func):
    # Envuelve la función original para agregar la comprobación de rol.
    def _wrapped_view_func(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != "TEACHER":
            # Si el usuario no es un profesor, devuelve un error de acceso prohibido.
            return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func

# Función para transformar ecuaciones antes de su procesamiento
def transformar_ecuacion(ecuacion_str):
    # Añade un espacio entre números y variables/operadores para facilitar el procesamiento de la ecuación.
    ecuacion_str = ecuacion_str.replace("x", " * x")
    ecuacion_str = ecuacion_str.replace("//", "/")
    return ecuacion_str

# Vista simple para pruebas y demostración
def some_view(request):
    # Envía un mensaje de éxito y muestra una plantilla de prueba.
    messages.success(request, "Esto es una prueba")
    return render(request, 'some_template.html')

# Vista para el registro de nuevos usuarios
def register_view(request):
    # Procesa el formulario de registro de usuarios.
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Guarda el nuevo usuario y redirige a la página de inicio de sesión.
            form.save()
            messages.success(request, "¡Usuario registrado con éxito! Por favor, inicie sesión.")
            return redirect('login')
    else:
        # Muestra un formulario de registro vacío si no es una solicitud POST.
        form = CustomUserCreationForm()
    return render(request, 'registro.html', {'form': form})

# Vista para el inicio de sesión de usuarios
def login_view(request):
    # Procesa el formulario de inicio de sesión.
    if request.method == 'POST':
        # Obtiene las credenciales proporcionadas por el usuario.
        email = request.POST.get('email')
        password = request.POST.get('password')
        if 'continue_as_guest' in request.POST:
            # Permite a los usuarios continuar como invitados si así lo eligen.
            user = authenticate(request, username="invitado", password="password_del_invitado")
        else:
            # Autentica al usuario con las credenciales proporcionadas.
            user = authenticate(request, email=email, password=password)
        if user:
            # Si la autenticación es exitosa, inicia sesión y redirige a la página de bienvenida.
            login(request, user)
            return redirect('bienvenido')
        else:
            # Si falla la autenticación, muestra un mensaje de error.
            messages.error(request, 'Email o contraseña inválidos')
    return render(request, 'login.html')

# Vista de bienvenida para usuarios autenticados
def bienvenido_view(request):
    # Muestra una página de bienvenida personalizada según si el usuario está autenticado o no.
    context = {'username': request.user.username if request.user.is_authenticated else "invitado"}
    return render(request, 'bienvenido.html', context)

# Vista de bienvenida para usuarios invitados
def bienvenido_invitado_view(request):
    # Muestra una página de bienvenida específica para usuarios invitados.
    return render(request, 'bienvenido_invitado.html')

# Vista para cerrar la sesión del usuario
def logout_view(request):
    # Cierra la sesión del usuario y redirige a la página de inicio de sesión.
    logout(request)
    return redirect('login')

# Vista para funcionalidad de arrastrar y soltar
def drag_drop_view(request):
    # Muestra una página con funcionalidad de arrastrar y soltar.
    return render(request, 'drag_and_drop.html')

# Vista para crear ecuaciones (solo accesible por profesores)
@login_required
@teacher_required
def crear_ecuacion(request):
    # Muestra una página para que los profesores creen nuevas ecuaciones.
    return render(request, 'ingresar_ecuacion.html')

# Vista para crear salones (solo accesible por profesores)
@login_required
@teacher_required
def crear_salon(request):
    # Procesa el formulario para crear nuevos salones.
    if request.method == "POST":
        form = SalonForm(request.POST)
        if form.is_valid():
            # Guarda el nuevo salón y redirige para agregar estudiantes.
            salon = form.save(commit=False)
            salon.profesor = request.user
            salon.save()
            return redirect('agregar_estudiante', salon_id=salon.id)
    else:
        # Muestra un formulario vacío si no es una solicitud POST.
        form = SalonForm()
    return render(request, 'class.html', {'form': form})

# Vista para agregar estudiantes a un salón específico
def agregar_estudiante(request, salon_id):
    # Obtiene el salón específico o devuelve un error si no existe.
    salon = get_object_or_404(Salon, id=salon_id)
    if request.method == "POST":
        form = AgregarEstudianteForm(request.POST)
        if form.is_valid():
            # Agrega los estudiantes seleccionados al salón y redirige a la lista de salones del profesor.
            estudiantes = form.cleaned_data['estudiantes']
            for estudiante in estudiantes:
                salon.estudiantes.add(estudiante)
            return redirect('mis_salones')
    else:
        # Muestra un formulario vacío si no es una solicitud POST.
        form = AgregarEstudianteForm()
    return render(request, 'agregar_estudiante.html', {'form': form, 'salon': salon})

# Vista para mostrar los salones de un profesor
@login_required
def mis_salones(request):
    # Obtiene todos los salones creados por el profesor actual.
    salones = Salon.objects.filter(profesor=request.user)
    return render(request, 'mis_clases.html', {'salones': salones})

# Vista para mostrar detalles de un salón específico
@login_required
def detalle_salon(request, salon_id):
    # Obtiene el salón específico o muestra un error si no existe.
    try:
        salon = Salon.objects.get(id=salon_id, profesor=request.user)
    except Salon.DoesNotExist:
        return HttpResponseNotFound("Salón no encontrado.")
    # Obtiene los estudiantes y actividades del salón.
    estudiantes = salon.estudiantes.all()
    actividades = Actividad.objects.filter(salon=salon)
    return render(request, 'detalle_salon.html', {'salon': salon, 'estudiantes': estudiantes, 'actividades': actividades})

# Vista para el perfil del usuario
def profile_view(request):
    # Procesa el formulario de perfil del usuario.
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            # Guarda los cambios en el perfil del usuario.
            form.save()
            return redirect('profile')
    else:
        # Muestra un formulario con la información actual del usuario.
        form = UserProfileForm(instance=request.user)

    # Obtiene las clases a las que el usuario está asignado.
    clases_asignadas = Salon.objects.filter(estudiantes=request.user)
    context = {
        'form': form,
        'clases_asignadas': clases_asignadas
    }
    return render(request, 'profile.html', context)

# Vista para listar ecuaciones creadas por un profesor
@login_required
@teacher_required
def listar_ecuaciones(request):
    # Obtiene todas las ecuaciones creadas por el profesor actual.
    ecuaciones = Ecuacion.objects.filter(profesor=request.user)
    return render(request, 'lista_ecuaciones.html', {'ecuaciones': ecuaciones})

# Función para generar ecuaciones aleatorias
def generar_ecuacion():
    # Elige números y operaciones aleatorios para crear ecuaciones.
    a = random.randint(1, 999)
    b = random.randint(1, 999)
    operacion = random.choice(['+', '-', '*', '//'])
    if operacion == '//':
        b = random.randint(1, 999)
    ecuacion_str = f"{a}x {operacion} {b} = 0" if operacion != '//' else f"{a * b}x // {b} = 0"
    return ecuacion_str

# Vista para crear actividades en un salón (accesible solo por profesores)
@login_required
@teacher_required
def crear_actividad(request, salon_id):
    # Obtener el salón específico por su ID.
    salon = Salon.objects.get(pk=salon_id)

    if request.method == "POST":
        form = ActividadForm(request.POST)
        if form.is_valid():
            # Número de ecuaciones a generar como parte de la actividad.
            numero_ecuaciones = form.cleaned_data['numero_ecuaciones']
            # Crear una nueva actividad vinculada al salón.
            actividad = Actividad.objects.create(salon=salon)
            
            # Generar las ecuaciones especificadas y añadirlas a la actividad.
            for _ in range(numero_ecuaciones):
                ecuacion_str = generar_ecuacion()
                ecuacion = Ecuacion.objects.create(ecuacion=ecuacion_str, profesor=request.user)
                actividad.ecuaciones.add(ecuacion)

            # Redireccionar a la vista detallada del salón.
            return redirect('detalle_salon', salon_id=salon.id)
    else:
        form = ActividadForm()

    return render(request, 'crear_actividad.html', {'form': form, 'salon': salon})

@login_required
def actividades_estudiante(request):
    estudiante = request.user

    # Obtener actividades que no han sido completadas por el estudiante.
    actividades_no_completadas = Actividad.objects.filter(
        salon__estudiantes=estudiante
    ).exclude(
        progresos__estudiante=estudiante, progresos__completada=True
    )

    # Renderizar la vista con las actividades pendientes.
    return render(request, 'actividades_estudiante.html', {'actividades': actividades_no_completadas})

@login_required
def enviar_respuestas(request, actividad_id):
    if request.method == "POST":
        actividad = get_object_or_404(Actividad, id=actividad_id)
        estudiante = request.user
        x = symbols('x')
        resultado_respuestas = {}

        for ecuacion in actividad.ecuaciones.all():
            respuesta = request.POST.get(f"respuesta_{ecuacion.id}")

            try:
                # Transforma y resuelve la ecuación.
                ecuacion_transformada = transformar_ecuacion(ecuacion.ecuacion.split('=')[0])
                solucion = solve(Eq(sympify(ecuacion_transformada), 0), x)[0]

                # Comprueba si la respuesta del estudiante es correcta.
                es_correcta = comparar_respuestas(respuesta, solucion)
                if not es_correcta:
                    # Si la respuesta es incorrecta, genera una pista.
                    pista, ejemplo = generar_pista(ecuacion)
                    resultado_respuestas[f"respuesta_{ecuacion.id}"] = {"correcta": es_correcta, "pista": pista, "ejemplo": ejemplo}
            except SympifyError:
                pista = "Hubo un error al analizar la ecuación."

            resultado_respuestas[f"respuesta_{ecuacion.id}"] = {"correcta": es_correcta, "pista": pista}

        # Envía las respuestas y pistas como un objeto JSON.
        return JsonResponse({"respuestas": resultado_respuestas})
    else:
        # Si no es un método POST, redirige a la lista de actividades del estudiante.
        return redirect('actividades_estudiante')

# Funciones para agregar o quitar puntos a un usuario específico.
def agregar_puntos(request, username):
    usuario = get_object_or_404(CustomUser, username=username)
    usuario.points += 50  
    usuario.save()
    return HttpResponse("Puntos añadidos correctamente.")

def quitar_puntos(request, username):
    usuario = get_object_or_404(CustomUser, username=username)
    usuario.points -= 50  
    usuario.save()
    return HttpResponse("Puntos restados correctamente.")

# Genera pistas basadas en el tipo de operación en la ecuación.
def generar_pista(ecuacion_obj):
    ecuacion_str = ecuacion_obj.ecuacion
    pista = ""
    ejemplo = ""

    # Proporciona pistas específicas según el operador en la ecuación.
    if '+' in ecuacion_str or '-' in ecuacion_str:
        # Pistas para ecuaciones con suma o resta.
        pista = "Realiza la misma operación en ambos lados de la ecuación para despejar 'x'."
        if '+' in ecuacion_str:
            ejemplo = "Por ejemplo, en '3x + 5 = 0', resta 5 en ambos lados para obtener '3x = -5'."
        elif '-' in ecuacion_str:
            ejemplo = "Por ejemplo, en '3x - 5 = 0', suma 5 en ambos lados para obtener '3x = 5'."
    elif '*' in ecuacion_str:
        # Pistas para ecuaciones con multiplicación.
        pista = "Si un lado de una ecuación multiplicativa es 0, el otro lado también debe ser 0."
        ejemplo = "Por ejemplo, en '2x * 3 = 0', ya que 2x * 3 es igual a 0, entonces 'x' debe ser 0."
    elif '/' in ecuacion_str:
        # Pistas para ecuaciones con división.
        pista = "Para resolver una división por cero, el numerador debe ser 0."
        ejemplo = "Por ejemplo, en 'x / 4 = 0', multiplica ambos lados por 4 para obtener 'x = 0'."
    else:
        # Pistas generales para otras ecuaciones.
        pista = "Revisa cómo has despejado la variable 'x' en la ecuación."
        ejemplo = "Intenta simplificar la ecuación paso a paso."

    return pista, ejemplo
