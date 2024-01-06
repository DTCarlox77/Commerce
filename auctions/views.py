from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import logout, authenticate, login as auth_login
from .models import CustomUser, Subasta, Oferta, Comentario, Watchlist
from django.db import IntegrityError
from django.db.models import Max

# Create your views here.
def main(request):
    categorias = Subasta.objects.values_list('categoria', flat=True).distinct()
    
    return render(request, 'index.html', {
        'categorias' : categorias
    })

# Muestra todos los productos activos disponibles para subastar.
def auctions(request):
    productos = Subasta.objects.filter(activo=True).order_by('-fecha')
    categorias = Subasta.objects.values_list('categoria', flat=True).distinct()
    
    if request.method == 'POST':
        busqueda = request.POST.get('search')
        
        if busqueda:
            # Muestra todos los productos.
            productos = Subasta.objects.filter(producto__icontains=busqueda).order_by('-fecha')
    
    return render(request, 'auctions.html', {
        'productos' : productos,
        'categorias' : categorias,
        'principal' : True,
    })

# Retorna productos según su categoría.
def category(request, filtro):
    productos = Subasta.objects.filter(categoria__icontains=filtro).order_by('-fecha')
    categorias = Subasta.objects.values_list('categoria', flat=True).distinct()

    return render(request, 'auctions.html', {
        'productos': productos,
        'categorias': categorias
    })

# Agrega o quita productos de la lista de seguimiento.
def add_remove_list(request, id):
    lista = Watchlist.objects.filter(usuario=request.user, producto=id)
    producto = get_object_or_404(Subasta, id=id)
    
    if lista.exists():
        lista.delete()
    
    else:
        if producto.vendedor != request.user:
            agrega_lista = Watchlist(usuario=request.user, producto=producto)
            agrega_lista.save()
    
    return redirect('product', id=id)

# Muestra una interfaz de múltiples opciones para cada producto.
def product(request, id):
    producto = get_object_or_404(Subasta, id=id)
    categorias = Subasta.objects.values_list('categoria', flat=True).distinct()
    en_lista = False
    comentarios = Comentario.objects.filter(producto=producto).order_by('-fecha')
    ofertas = Oferta.objects.filter(producto=producto)
    ofertas_usuario = None
    oferta_maxima = None
    mensaje = None
    oferta_maxima_usuario = None
    
    if request.user.is_authenticated:
        lista = Watchlist.objects.filter(usuario=request.user, producto=producto)
        ofertas_usuario = Oferta.objects.filter(producto=producto, usuario=request.user)
        oferta_maxima = ofertas.aggregate(Max('oferta'))['oferta__max']
        en_lista = lista.exists()
        oferta_maxima_usuario = ofertas_usuario.aggregate(Max('oferta'))['oferta__max']
        
        if oferta_maxima_usuario:
            oferta_maxima_usuario = round(oferta_maxima_usuario, 2)
            
        if oferta_maxima:
            oferta_maxima = round(oferta_maxima, 2)
        
    if request.method == 'POST':
        oferta = request.POST.get('oferta')
        
        try:
            oferta = float(oferta)
            
            if oferta >= producto.precio_inicial and (not oferta_maxima or oferta > oferta_maxima):
                try:
                    nueva_oferta = Oferta(usuario=request.user, producto=producto, oferta=oferta)
                    nueva_oferta.save()
                    mensaje = ('Tu oferta se ha agregado exitosamente', 0)
                    producto.precio_venta = oferta
                    producto.save()
                    
                    # Actualización de las variables de oferta.
                    ofertas_usuario = Oferta.objects.filter(producto=producto, usuario=request.user)
                    oferta_maxima = ofertas.aggregate(Max('oferta'))['oferta__max']
                    oferta_maxima = round(oferta_maxima, 2)
                    oferta_maxima_usuario = ofertas_usuario.aggregate(Max('oferta'))['oferta__max']
                    oferta_maxima_usuario = round(oferta_maxima_usuario, 2)
                    
                except:
                    mensaje = ('No hemos podido almacenar tu oferta', 1)
            else:
                mensaje = ('Error: El precio a ofertar no es válido', 1)
                        
        except:
            mensaje = ('Algo salió mal', 1)
        
    return render(request, 'product.html', {
        'producto' : producto,
        'categorias' : categorias,
        'en_lista': en_lista,
        'comentarios' : comentarios,
        'ofertas' : ofertas,
        'mensaje' : mensaje,
        'cantidad_ofertas' : ofertas.count(),
        'oferta_maxima' : oferta_maxima,
        'oferta_maxima_usuario' : oferta_maxima_usuario
    })

# Vista para el anexo de comentarios en un producto.
@login_required
def comment(request, id):
    producto = get_object_or_404(Subasta, id=id)
    
    if request.method == 'POST':
        comentario = request.POST.get('comentario')
        nuevo_comentario = Comentario(usuario=request.user, comentario=comentario, producto=producto)
        nuevo_comentario.save()
    
    return redirect('product', id)

# Formulario para agregar productos en la plataforma.
@login_required
def new_product(request):
    # Cero retorna un sucess mientras que uno retorna incorrecto.
    respaldo = dict()
    mensaje = None
    
    categorias = Subasta.objects.values_list('categoria', flat=True).distinct()
    todas_categorias = Subasta.categorias
    
    if request.method == 'POST':
        producto = request.POST.get('producto')
        descripcion = request.POST.get('descripcion')
        categoria = request.POST.get('categoria')
        imagen = request.POST.get('imagen')
        precio_inicial = request.POST.get('precio_inicial')
        
        if not imagen:
            imagen = 'https://www.nbmchealth.com/wp-content/uploads/2018/04/default-placeholder.png'
            
        if not categoria:
            categoria = 'Sin especificar'
        
        respaldo = {
            'producto' : producto,
            'descripcion' : descripcion,
            'categoria' : categoria,
            'imagen' : imagen,
            'precio_inicial' : precio_inicial
        }
        
        # Convierte la cadena del formulario en un valor flotante.
        try:
            precio_inicial = float(precio_inicial)
            
        except:
            precio_inicial = None
        
        if precio_inicial:
            if precio_inicial <= 0 or precio_inicial > 1000000:
                mensaje = ['El precio ingresado no es válido', 1]
        
        if not precio_inicial or not producto or not descripcion:
            mensaje = ['Debes completar todos los campos', 1]
            
        try:
            producto = Subasta(producto=producto, vendedor=request.user, descripcion=descripcion, categoria=categoria, imagen=imagen, precio_inicial=precio_inicial)
            respaldo = None
            mensaje = ['Producto agregado correctamente', 0]
            producto.save()
        
        except IntegrityError as e:
            mensaje = 'Algo salió mal :/'
    
    return render(request, 'new.html', {
        'categorias' : categorias,
        'todas_categorias' : todas_categorias,
        'respaldo' : respaldo,
        'mensaje' : mensaje
    })

# Inicio de sesión.
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

# Registro de cuenta con validaciones.
@csrf_protect
def sign_in(request):
    if request.user.is_authenticated:
        return redirect('main')
    
    categorias = Subasta.objects.values_list('categoria', flat=True).distinct()
    
    if request.method == 'POST':
        # Validación de los datos del formulario.
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        respaldo = {
            'username': username,
            'password': password,
            'categorias' : categorias
        }

        if not username or not password:
            return render(request, 'registration/sign_in.html', {
                'mensaje': 'Completa todos los campos para registrarte',
                'respaldo': respaldo,
                'categorias' : categorias
            })
    
        if not username.isalnum():
            return render(request, 'registration/sign_in.html', {
                'mensaje': 'El nombre de usuario no puede contener caracteres especiales',
                'respaldo': respaldo,
                'categorias' : categorias
            })
        
        if len(password) < 5:
            return render(request, 'registration/sign_in.html', {
                'mensaje': 'La contraseña ingresada es muy corta',
                'respaldo': respaldo,
                'categorias' : categorias
            })
            
        try:
            user = CustomUser.objects.create_user(username=username, password=password)
            return redirect('login')
        
        except IntegrityError as e:
            if 'UNIQUE constraint' in str(e):
                return render(request, 'registration/sign_in.html', {
                    'mensaje': 'El nombre de usuario ya está en uso. Por favor, elige otro.',
                    'respaldo': respaldo,
                    'categorias' : categorias
                })
            else:
                return render(request, 'registration/sign_in.html', {
                    'mensaje': f'Error de registro: {e}',
                    'respaldo': respaldo,
                    'categorias' : categorias
                })
            
    return render(request, 'registration/sign_in.html', {
        'categorias' : categorias
    })

# Devuelve los objetos creados por el usuario.
@login_required
def user_products(request):
    productos = Subasta.objects.filter(vendedor=request.user).order_by('-fecha')
    categorias = Subasta.objects.values_list('categoria', flat=True).distinct()
    
    return render(request, 'auctions.html', {
        'productos' : productos,
        'categorias' : categorias,
        'myproducts' : True
    })

# Devuelve los objetos agregados a la lista de seguimiento.
@login_required
def watch_list(request):
    # Obtiene los objetos de la lista de seguimiento.
    productos = Subasta.objects.filter(watchlist__usuario=request.user).order_by('-fecha').distinct()
    categorias = Subasta.objects.values_list('categoria', flat=True).distinct()
    
    return render(request, 'auctions.html', {
        'productos' : productos,
        'categorias' : categorias,
        'watchlist' : True
    })

# Se encarga de finalizar una subasta activa.
@login_required
def close_auction(request, id):
    
    producto = get_object_or_404(Subasta, id=id)
    
    if request.user == producto.vendedor:
        producto.activo = False
        producto.save()

    return redirect('product', id)

# Cierra la sesión de usuario.
@login_required
def close(request):
    
    logout(request)
    return redirect('login')