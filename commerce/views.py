from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import logout, authenticate, login as auth_login
from .models import CustomUser, Subasta, Oferta, Comentario
from django.db import IntegrityError

# Create your views here.
def main(request):
    
    return render(request, 'index.html')

def auctions(request):
    
    productos = Subasta.objects.all()
    categorias = Subasta.objects.values_list('categoria', flat=True).distinct()
    
    return render(request, 'auctions.html', {
        'productos' : productos,
        'categorias' : categorias
    })

def product(request, id):
    
    producto = get_object_or_404(Subasta, id=id)
    categorias = Subasta.objects.values_list('categoria', flat=True).distinct()
    
    return render(request, 'product.html', {
        'producto' : producto,
        'categorias' : categorias
    })

@login_required
def comment(request, id):
    
    return render(request, 'product.html')

@login_required
def new_product(request):
    
    return render(request, 'new.html')

@csrf_protect
def login(request):
    
    if request.user.is_authenticated:
        return redirect('main')
    
    if request.method == 'POST':
        # Validación de los datos del formulario.
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            
            # Verifica si existe una ruta de redirección (next).
            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url:
                return redirect(next_url)
            
            # Si no hay una ruta de redirección, redirigir a 'auctions'.
            return redirect('auctions')
        
        else:
            return render(request, 'registration/login.html', {'mensaje': 'Credenciales incorrectas. Por favor, inténtalo de nuevo.'})
    
    return render(request, 'registration/login.html')

def sign_in(request):
    
    if request.user.is_authenticated:
        return redirect('main')
    
    if request.method == 'POST':
        # Validación de los datos del formulario.
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        respaldo = {
            'username': username,
            'password': password,
        }

        if not username or not password:
            return render(request, 'registration/sign_in.html', {
                'mensaje': 'Completa todos los campos para registrarte',
                'respaldo': respaldo
            })
    
        if not username.isalnum():
            return render(request, 'registration/sign_in.html', {
                'mensaje': 'El nombre de usuario no puede contener caracteres especiales',
                'respaldo': respaldo
            })
        
        if len(password) < 5:
            return render(request, 'registration/sign_in.html', {
                'mensaje': 'La contraseña ingresada es muy corta',
                'respaldo': respaldo
            })
            
        try:
            user = CustomUser.objects.create_user(username=username, password=password)
            return redirect('login')
        
        except IntegrityError as e:
            if 'UNIQUE constraint' in str(e):
                return render(request, 'registration/sign_in.html', {
                    'mensaje': 'El nombre de usuario ya está en uso. Por favor, elige otro.',
                    'respaldo': respaldo
                })
            else:
                return render(request, 'registration/sign_in.html', {
                    'mensaje': f'Error de registro: {e}',
                    'respaldo': respaldo
                })
            
    return render(request, 'registration/sign_in.html')

@login_required
def user_products(request):
    
    return render(request, 'auctions.html')

@login_required
def watch_list(request):
    
    return render(request, 'auctions.html')

def category(request, filtro):
    
    return render(request, 'auctions.html')

@login_required
def close(request):
    
    logout(request)
    return redirect('login')