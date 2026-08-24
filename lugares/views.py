import json

from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render

from mapas.models import PuntoInteres
from rutas.models import Ruta

from .models import Lugar

# Centro aproximado del cantón La Maná, usado cuando no hay lugares que centrar.
CENTRO_LA_MANA = {"lat": -0.9431, "lng": -79.2312}


def mapa(request):
    """Mapa web interactivo con lugares recreativos, puntos de interés
    (recursos naturales e infraestructura) y rutas de acceso."""
    lugares = Lugar.objects.select_related("categoria").order_by("nombre")

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
