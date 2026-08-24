from django.contrib import admin

from .models import Categoria, Evento, Lugar


@admin.action(description="Marcar seleccionados como aprobados")
def marcar_aprobado(modeladmin, request, queryset):
    queryset.update(aprobado=True)


@admin.action(description="Marcar seleccionados como NO aprobados")
def marcar_no_aprobado(modeladmin, request, queryset):
    queryset.update(aprobado=False)


@admin.register(Lugar)
class LugarAdmin(admin.ModelAdmin):
    list_display = ("nombre", "categoria", "aprobado", "creado_por", "fecha_creacion")
    list_filter = ("aprobado", "categoria")
    search_fields = ("nombre", "direccion")
    actions = [marcar_aprobado, marcar_no_aprobado]


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "lugar", "aprobado", "creado_por", "fecha_inicio", "fecha_fin")
    list_filter = ("aprobado",)
    search_fields = ("nombre", "lugar__nombre")
    actions = [marcar_aprobado, marcar_no_aprobado]


admin.site.register(Categoria)
