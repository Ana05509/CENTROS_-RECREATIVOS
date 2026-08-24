import json

from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import redirect, render

from mapas.models import PuntoInteres
from rutas.models import Ruta

from .forms import SugerenciaEventoForm, SugerenciaLugarForm
from .models import Categoria, Lugar

# Centro aproximado del cantón La Maná, usado cuando no hay lugares que centrar.
CENTRO_LA_MANA = {"lat": -0.9431, "lng": -79.2312}


def inicio(request):
    """Portal público: presentación del proyecto, accesos a mapa, cuenta
    y sugerencias, más un resumen de lo que hay cargado hasta ahora."""
    stats = {
        "lugares": Lugar.objects.filter(aprobado=True).count(),
        "categorias": Categoria.objects.count(),
        "puntos": PuntoInteres.objects.count(),
        "rutas": Ruta.objects.count(),
    }
    return render(request, "lugares/inicio.html", {"stats": stats})


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
            "imagen": lugar.imagen.url if lugar.imagen else None,
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

    context = {
        "lugares_json": json.dumps(lugares_json, cls=DjangoJSONEncoder),
        "puntos_json": json.dumps(puntos_json, cls=DjangoJSONEncoder),
        "rutas_json": json.dumps(rutas_json, cls=DjangoJSONEncoder),
        "categorias": categorias,
        "total_lugares": len(lugares_json),
        "centro": CENTRO_LA_MANA,
    }
    return render(request, "lugares/mapa.html", context)


def sugerir(request):
    """Formulario público para proponer un lugar o un evento nuevo.
    Queda pendiente de aprobación (aprobado=False) hasta que el admin
    lo revisa desde el panel de administración."""
    lugar_form = SugerenciaLugarForm(prefix="lugar")
    evento_form = SugerenciaEventoForm(prefix="evento")
    tipo_activo = "lugar"

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
        "tipo_activo": tipo_activo,
    }
    return render(request, "lugares/sugerir.html", context)
