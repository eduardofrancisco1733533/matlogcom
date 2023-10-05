from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm
from django.contrib import messages

# Una vista simple que muestra un mensaje de éxito y renderiza una plantilla
def some_view(request):
    messages.success(request, "Esto es una prueba")
    return render(request, 'some_template.html')

# Vista para registrar a un nuevo usuario
def register_view(request):
    if request.method == 'POST':  # Si el formulario se envía
        form = CustomUserCreationForm(request.POST)  # Se instancia el formulario con los datos enviados
        if form.is_valid():  # Verifica si el formulario es válido
            user = form.save()  # Guarda el usuario en la base de datos
            messages.success(request, "¡Usuario registrado con éxito! Por favor, inicie sesión.")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registro.html', {'form': form})

# Vista para iniciar sesión
def login_view(request):
    if request.method == 'POST':  # Si el formulario de inicio de sesión se envía
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Si el usuario decide continuar como invitado
        if 'continue_as_guest' in request.POST:
            user = authenticate(request, username="invitado", password="password_del_invitado")
        else:  # De lo contrario, autentica con el correo y la contraseña proporcionados
            user = authenticate(request, email=email, password=password)

        if user:  # Si la autenticación es exitosa
            login(request, user)  # Inicia sesión
            return redirect('bienvenido')
        else:  # Si la autenticación falla
            messages.error(request, 'Email o contraseña inválidos')
    return render(request, 'login.html')

# Vista que muestra la página de bienvenida al usuario
def bienvenido_view(request):
    context = {}
    if not request.user.is_authenticated:  # Si el usuario no ha iniciado sesión
        context['username'] = "invitado"
    else:
        context['username'] = request.user.username
    return render(request, 'bienvenido.html', context)

# Vista de bienvenida específica para usuarios invitados
def bienvenido_invitado_view(request):
    return render(request, 'bienvenido_invitado.html')

# Vista para cerrar sesión
def logout_view(request):
    logout(request)
    return redirect('login')

# Vista relacionada con una funcionalidad de "arrastrar y soltar"
def drag_drop_view(request):
    return render(request, 'drag_and_drop.html')
