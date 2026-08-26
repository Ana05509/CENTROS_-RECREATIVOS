from django.contrib import admin

from .models import PuntoInteres


@admin.register(PuntoInteres)
class PuntoInteresAdmin(admin.ModelAdmin):
    list_display = ("nombre", "tipo", "subtipo", "fecha_creacion")
    list_filter = ("tipo",)
    search_fields = ("nombre", "subtipo")
    list_per_page = 30
