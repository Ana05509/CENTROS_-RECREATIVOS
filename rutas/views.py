from django.shortcuts import render

from .models import Ruta


def lista(request):
    """Catálogo público de rutas de acceso hacia los lugares recreativos."""
    rutas = Ruta.objects.select_related("lugar").order_by("lugar__nombre")
    context = {"rutas": rutas, "nav_activo": "rutas"}
    return render(request, "rutas/lista.html", context)
