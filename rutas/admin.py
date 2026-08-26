from django.contrib import admin

from .models import Ruta


@admin.register(Ruta)
class RutaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "lugar", "tipo_transporte", "distancia_km", "tiempo_estimado")
    list_filter = ("tipo_transporte",)
    search_fields = ("nombre", "lugar__nombre", "punto_partida")
    list_per_page = 30
    autocomplete_fields = ("lugar",)
