from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from django.utils.html import format_html

from .models import (
    EXTENSIONES_MULTIMEDIA_PERMITIDAS,
    TAMANO_MAXIMO_MULTIMEDIA_MB,
    Categoria,
    Evento,
    Lugar,
    Multimedia,
    TipoMultimedia,
)

admin.site.site_header = "Mapa Recreativo de La Maná"
admin.site.site_title = "Admin — Mapa Recreativo"
admin.site.index_title = "Panel de administración"


def vista_manual(request):
    """Manual del administrador, dentro del propio /admin/."""
    context = {
        **admin.site.each_context(request),
        "title": "Manual del administrador",
        "extensiones_multimedia": ", ".join(EXTENSIONES_MULTIMEDIA_PERMITIDAS),
        "tamano_maximo_mb": TAMANO_MAXIMO_MULTIMEDIA_MB,
    }
    return render(request, "admin/manual.html", context)


# Se agrega la URL del manual al admin sin necesidad de crear un AdminSite
# propio: se envuelve get_urls() del sitio por defecto, tal como recomienda
# la documentación de Django para agregar vistas extra al admin.
_get_urls_original = admin.site.get_urls


def _get_urls_con_manual():
    urls_extra = [
        path("manual/", admin.site.admin_view(vista_manual), name="manual"),
    ]
    return urls_extra + _get_urls_original()


admin.site.get_urls = _get_urls_con_manual


@admin.action(description="Marcar seleccionados como aprobados")
def marcar_aprobado(modeladmin, request, queryset):
    queryset.update(aprobado=True)


@admin.action(description="Marcar seleccionados como NO aprobados")
def marcar_no_aprobado(modeladmin, request, queryset):
    queryset.update(aprobado=False)


@admin.register(Lugar)
class LugarAdmin(admin.ModelAdmin):
    list_display = ("miniatura", "nombre", "categoria", "parroquia", "aprobado", "creado_por", "fecha_creacion")
    list_display_links = ("miniatura", "nombre")
    list_editable = ("aprobado",)
    list_filter = ("aprobado", "categoria", "parroquia")
    search_fields = ("nombre", "direccion", "parroquia")
    date_hierarchy = "fecha_creacion"
    list_per_page = 30
    actions = [marcar_aprobado, marcar_no_aprobado]

    @admin.display(description="Foto")
    def miniatura(self, lugar):
        if lugar.imagen:
            return format_html(
                '<img src="{}" style="width:44px;height:44px;object-fit:cover;border-radius:6px;">',
                lugar.imagen.url,
            )
        return "—"


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "lugar", "aprobado", "creado_por", "fecha_inicio", "fecha_fin")
    list_editable = ("aprobado",)
    list_filter = ("aprobado",)
    search_fields = ("nombre", "lugar__nombre")
    date_hierarchy = "fecha_inicio"
    list_per_page = 30
    actions = [marcar_aprobado, marcar_no_aprobado]


@admin.register(Multimedia)
class MultimediaAdmin(admin.ModelAdmin):
    list_display = ("miniatura", "lugar", "tipo", "aprobado", "creado_por", "fecha_creacion")
    list_display_links = ("miniatura", "lugar")
    list_editable = ("aprobado",)
    list_filter = ("aprobado", "tipo")
    search_fields = ("lugar__nombre", "descripcion")
    date_hierarchy = "fecha_creacion"
    list_per_page = 30
    actions = [marcar_aprobado, marcar_no_aprobado]

    @admin.display(description="Vista previa")
    def miniatura(self, media):
        if media.tipo == TipoMultimedia.FOTO and media.archivo:
            return format_html(
                '<img src="{}" style="width:44px;height:44px;object-fit:cover;border-radius:6px;">',
                media.archivo.url,
            )
        if media.tipo == TipoMultimedia.VIDEO:
            return "🎬"
        return "—"


admin.site.register(Categoria)
