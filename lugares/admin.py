from django.contrib import admin
from .models import Categoria, Lugar, Evento

admin.site.register(Categoria)
admin.site.register(Lugar)
admin.site.register(Evento)