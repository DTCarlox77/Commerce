from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

class CustomUser(AbstractUser):

    def __str__(self):
        return self.username

class Subasta(models.Model):
    categorias = [
        ('Sin especificar', 'Sin especificar'),
        ('Juguetes', 'Juguetes'),
        ('Ropa', 'Ropa'),
        ('Electrónica', 'Electrónica'),
        ('Hogar', 'Hogar'),
        ('Colección', 'Colección'),
        ('Videojuegos', 'Videojuegos'),
        ('Tecnología', 'Tecnología'),
        ('Cocina', 'Cocina'),
        ('Decoración', 'Decoración'),
        ('Medicina', 'Medicina'),
        ('Accesorios', 'Accesorios')
    ]

    producto = models.CharField(max_length=40, null=False)
    descripcion = models.TextField()
    categoria = models.CharField(max_length=30, choices=categorias)
    imagen = models.CharField(max_length=256)
    precio_inicial = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.5)])
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    vendedor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='usuario_vendedor')
    fecha = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.producto} subido por {self.vendedor}'

class Comentario(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='usuario_comentario')
    producto = models.ForeignKey(Subasta, on_delete=models.CASCADE, related_name='producto_comentario')
    comentario = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.usuario} ha hecho un comentario en {self.id} - {self.producto}'

class Oferta(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='usuario_oferta')
    producto = models.ForeignKey(Subasta, on_delete=models.CASCADE, related_name='producto_oferta')
    oferta = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.usuario} ha ofertado en {self.producto}'
    
class Watchlist(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    producto = models.ForeignKey(Subasta, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.usuario} ha agregado {self.producto} a la lista de seguimiento'