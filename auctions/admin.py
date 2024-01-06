from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Subasta)
admin.site.register(Oferta)
admin.site.register(Comentario)
admin.site.register(Watchlist)