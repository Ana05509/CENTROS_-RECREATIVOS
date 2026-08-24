from django.contrib import admin

from .models import PuntoInteres


@admin.register(PuntoInteres)
class PuntoInteresAdmin(admin.ModelAdmin):
    list_display = ("nombre", "tipo", "subtipo")
    list_filter = ("tipo",)
    search_fields = ("nombre", "subtipo")
