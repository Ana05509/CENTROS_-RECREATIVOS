import json

from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render

from .models import Lugar

# Centro aproximado del cantón La Maná, usado cuando no hay lugares que centrar.
CENTRO_LA_MANA = {"lat": -0.9431, "lng": -79.2312}


def mapa(request):
    """Mapa web interactivo con todos los lugares recreativos."""
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

    categorias = sorted({lugar.categoria.nombre for lugar in lugares})

    context = {
        "lugares_json": json.dumps(lugares_json, cls=DjangoJSONEncoder),
        "categorias": categorias,
        "total_lugares": len(lugares_json),
        "centro": CENTRO_LA_MANA,
    }
    return render(request, "lugares/mapa.html", context)
