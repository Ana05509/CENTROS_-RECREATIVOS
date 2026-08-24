from django.shortcuts import render

from .models import PuntoInteres, TipoPunto


def lista(request):
    """Catálogo público de recursos naturales e infraestructura del cantón."""
    puntos = PuntoInteres.objects.all().order_by("nombre")
    context = {
        "recursos_naturales": puntos.filter(tipo=TipoPunto.RECURSO_NATURAL),
        "infraestructura": puntos.filter(tipo=TipoPunto.INFRAESTRUCTURA),
        "nav_activo": "recursos",
    }
    return render(request, "mapas/lista.html", context)
