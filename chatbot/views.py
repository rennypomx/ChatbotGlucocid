from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout

def index(request):
    return render(request, 'index.html')

def inicio(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            # Redirige a Streamlit con el nombre de usuario como parámetro de consulta
            streamlit_url = f"http://localhost:8501/?username={user.username}"
            return redirect(streamlit_url)
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos')
            return render(request, 'login.html')
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        cedula = request.POST.get('cedula')  # Obtener la cédula
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        password_confirm = request.POST.get('password2')

        if password == password_confirm:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Este nombre de usuario ya está en uso.')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Este correo electrónico ya está registrado.')
            else:
                # Guardar la cédula en el campo 'first_name' como ejemplo
                user = User.objects.create_user(username=username, email=email, password=password)
                user.first_name = cedula  # Guardamos la cédula en 'first_name'
                user.save()
                auth_login(request, user)
                messages.success(request, 'Registro exitoso. Bienvenido a Glucocid!')
                return redirect('inicio')
        else:
            messages.error(request, 'Las contraseñas no coinciden.')
    return render(request, 'register.html')


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {
            'username': request.user.username,
            'email': request.user.email
        }
        return Response(content)
    
def logout_view(request):
    logout(request)  # Cierra la sesión del usuario
    return redirect('index')  # Redirige a la vista 'index'
