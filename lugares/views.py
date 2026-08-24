import json

from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count, Max, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from mapas.models import PuntoInteres
from rutas.models import Ruta

from .forms import SugerenciaEventoForm, SugerenciaLugarForm, SugerenciaMultimediaForm
from .models import Categoria, Lugar, TipoMultimedia

# Centro aproximado del cantón La Maná, usado cuando no hay lugares que centrar.
CENTRO_LA_MANA = {"lat": -0.9431, "lng": -79.2312}

# Ícono y tema visual (para el degradado de la tarjeta) por categoría, usados
# en la sección "Explora por categoría" del portal. Las categorías que no
# aparecen aquí caen en el tema/ícono por defecto.
TEMA_CATEGORIA = {
    "Cascadas": ("💦", "agua"),
    "Ríos": ("🏞️", "agua"),
    "Balnearios": ("🏊", "agua"),
    "Piscinas": ("🏊‍♂️", "agua"),
    "Parques Recreativos": ("🌳", "naturaleza"),
    "Canchas Deportivas": ("⚽", "naturaleza"),
    "Miradores": ("🔭", "naturaleza"),
    "Área de Camping": ("⛺", "naturaleza"),
    "Centros Vacacionales": ("🏨", "infraestructura"),
    "Complejos Turísticos": ("🎡", "infraestructura"),
}


def inicio(request):
    """Portal público: presentación del proyecto, accesos a mapa, cuenta
    y sugerencias, más un resumen de lo que hay cargado hasta ahora."""
    stats = [
        {
            "numero": Lugar.objects.filter(aprobado=True).count(),
            "etiqueta": "Lugares recreativos",
            "detalle": "para visitar y disfrutar",
            "icono": "📍",
            "color": "verde",
        },
        {
            "numero": Categoria.objects.count(),
            "etiqueta": "Categorías",
            "detalle": "de actividades y lugares",
            "icono": "🏷️",
            "color": "naranja",
        },
        {
            "numero": PuntoInteres.objects.count(),
            "etiqueta": "Recursos e infraestructura",
            "detalle": "para el esparcimiento",
            "icono": "💧",
            "color": "azul",
        },
        {
            "numero": Ruta.objects.count(),
            "etiqueta": "Rutas de acceso",
            "detalle": "para llegar fácilmente",
            "icono": "🔀",
            "color": "morado",
        },
    ]

    categorias_con_lugares = (
        Categoria.objects
        .annotate(total=Count("lugar", filter=Q(lugar__aprobado=True)))
        .filter(total__gt=0)
        .order_by("-total")
    )
    categorias_destacadas = [
        {
            "nombre": categoria.nombre,
            "total": categoria.total,
            "icono": TEMA_CATEGORIA.get(categoria.nombre, ("📍", "naturaleza"))[0],
            "tema": TEMA_CATEGORIA.get(categoria.nombre, ("📍", "naturaleza"))[1],
        }
        for categoria in categorias_con_lugares
    ]

    context = {"stats": stats, "categorias_destacadas": categorias_destacadas, "nav_activo": "inicio"}
    return render(request, "lugares/inicio.html", context)


def lista_lugares(request):
    """Catálogo público de todos los lugares recreativos aprobados,
    con filtro opcional por categoría."""
    categoria_nombre = request.GET.get("categoria", "")
    lugares = Lugar.objects.filter(aprobado=True).select_related("categoria").order_by("nombre")
    if categoria_nombre:
        lugares = lugares.filter(categoria__nombre=categoria_nombre)

    categorias = Categoria.objects.filter(lugar__aprobado=True).distinct().order_by("nombre")

    context = {
        "lugares": lugares,
        "categorias": categorias,
        "categoria_activa": categoria_nombre,
        "nav_activo": "lugares",
    }
    return render(request, "lugares/lista.html", context)


def mapa(request):
    """Mapa web interactivo con lugares recreativos, puntos de interés
    (recursos naturales e infraestructura) y rutas de acceso."""
    lugares = Lugar.objects.filter(aprobado=True).select_related("categoria").order_by("nombre")

    lugares_json = [
        {
            "id": lugar.id,
            "nombre": lugar.nombre,
            "descripcion": lugar.descripcion,
            "direccion": lugar.direccion,
            "lat": lugar.latitud,
            "lng": lugar.longitud,
            "horario": lugar.horario,
            "costo_entrada": str(lugar.costo_entrada),
            "categoria": lugar.categoria.nombre,
            "parroquia": lugar.parroquia,
            "imagen": lugar.imagen.url if lugar.imagen else None,
            "detalle_url": reverse("lugares:detalle", args=[lugar.id]),
            "multimedia_count": lugar.multimedia.filter(aprobado=True).count(),
        }
        for lugar in lugares
    ]

    puntos_json = [
        {
            "id": punto.id,
            "nombre": punto.nombre,
            "tipo": punto.tipo,
            "subtipo": punto.subtipo,
            "descripcion": punto.descripcion,
            "lat": punto.latitud,
            "lng": punto.longitud,
        }
        for punto in PuntoInteres.objects.all()
    ]

    rutas_json = [
        {
            "id": ruta.id,
            "nombre": ruta.nombre,
            "lugar": ruta.lugar.nombre,
            "punto_partida": ruta.punto_partida,
            "descripcion": ruta.descripcion,
            "tipo_transporte": ruta.get_tipo_transporte_display(),
            "distancia_km": ruta.distancia_km,
            "tiempo_estimado": ruta.tiempo_estimado,
            "trazado": ruta.trazado,
        }
        for ruta in Ruta.objects.select_related("lugar").all()
    ]

    categorias = sorted({lugar.categoria.nombre for lugar in lugares})

    # "Lugares destacados": una pequeña muestra mixta (lugares, recursos
    # naturales y rutas reales) para el carrusel flotante del mapa.
    destacados = []
    for lugar in lugares[:3]:
        destacados.append({
            "nombre": lugar.nombre,
            "etiqueta": "Recreativo",
            "color": "azul",
            "url": f"{reverse('lugares:mapa')}?lugar={lugar.id}",
        })
    for punto in PuntoInteres.objects.filter(tipo="recurso_natural")[:2]:
        destacados.append({
            "nombre": punto.nombre,
            "etiqueta": "Recurso natural",
            "color": "verde",
            "url": f"{reverse('lugares:mapa')}?punto={punto.id}",
        })
    for ruta in Ruta.objects.select_related("lugar")[:2]:
        destacados.append({
            "nombre": ruta.nombre,
            "etiqueta": "Ruta de acceso",
            "color": "morado",
            "url": f"{reverse('lugares:mapa')}?ruta={ruta.id}",
        })

    parroquias = sorted({lugar.parroquia for lugar in lugares if lugar.parroquia})

    ultima_actualizacion = lugares.aggregate(fecha=Max("fecha_creacion"))["fecha"]

    context = {
        "lugares_json": json.dumps(lugares_json, cls=DjangoJSONEncoder),
        "puntos_json": json.dumps(puntos_json, cls=DjangoJSONEncoder),
        "rutas_json": json.dumps(rutas_json, cls=DjangoJSONEncoder),
        "categorias": categorias,
        "parroquias": parroquias,
        "total_lugares": len(lugares_json),
        "total_puntos": len(puntos_json),
        "total_rutas": len(rutas_json),
        "total_categorias": Categoria.objects.count(),
        "ultima_actualizacion": ultima_actualizacion,
        "destacados": destacados,
        "centro": CENTRO_LA_MANA,
        "nav_activo": "mapa",
    }
    return render(request, "lugares/mapa.html", context)


def detalle_lugar(request, lugar_id):
    """Ficha de un lugar con su galería de fotos y videos aprobados."""
    lugar = get_object_or_404(Lugar, pk=lugar_id, aprobado=True)
    fotos = lugar.multimedia.filter(aprobado=True, tipo=TipoMultimedia.FOTO)
    videos = lugar.multimedia.filter(aprobado=True, tipo=TipoMultimedia.VIDEO)
    context = {"lugar": lugar, "fotos": fotos, "videos": videos}
    return render(request, "lugares/detalle.html", context)


def sugerir(request):
    """Formulario público para proponer un lugar, un evento, o una foto/video
    para un lugar ya existente. Queda pendiente de aprobación (aprobado=False)
    hasta que el admin lo revisa desde el panel de administración."""
    lugar_preseleccionado = request.GET.get("lugar")

    lugar_form = SugerenciaLugarForm(prefix="lugar")
    evento_form = SugerenciaEventoForm(prefix="evento")
    multimedia_form = SugerenciaMultimediaForm(
        prefix="multimedia",
        initial={"lugar": lugar_preseleccionado} if lugar_preseleccionado else None,
    )
    tipo_activo = "multimedia" if lugar_preseleccionado else "lugar"

    if request.method == "POST":
        # Honeypot: campo oculto que solo un bot llenaría.
        if request.POST.get("sitio_web"):
            return redirect("lugares:sugerir")

        tipo_activo = request.POST.get("tipo", "lugar")
        autor = request.user if request.user.is_authenticated else None

        if tipo_activo == "evento":
            evento_form = SugerenciaEventoForm(request.POST, request.FILES, prefix="evento")
            if evento_form.is_valid():
                evento = evento_form.save(commit=False)
                evento.aprobado = False
                evento.creado_por = autor
                evento.save()
                messages.success(
                    request,
                    "¡Gracias! Tu evento fue enviado y quedará visible apenas sea revisado.",
                )
                return redirect("lugares:sugerir")
        elif tipo_activo == "multimedia":
            multimedia_form = SugerenciaMultimediaForm(request.POST, request.FILES, prefix="multimedia")
            if multimedia_form.is_valid():
                media = multimedia_form.save(commit=False)
                media.aprobado = False
                media.creado_por = autor
                media.save()
                messages.success(
                    request,
                    "¡Gracias! Tu foto/video fue enviado y quedará visible apenas sea revisado.",
                )
                return redirect("lugares:sugerir")
        else:
            lugar_form = SugerenciaLugarForm(request.POST, request.FILES, prefix="lugar")
            if lugar_form.is_valid():
                lugar = lugar_form.save(commit=False)
                lugar.aprobado = False
                lugar.creado_por = autor
                lugar.save()
                messages.success(
                    request,
                    "¡Gracias! Tu lugar fue enviado y aparecerá en el mapa apenas sea revisado.",
                )
                return redirect("lugares:sugerir")

    context = {
        "lugar_form": lugar_form,
        "evento_form": evento_form,
        "multimedia_form": multimedia_form,
        "tipo_activo": tipo_activo,
    }
    return render(request, "lugares/sugerir.html", context)
