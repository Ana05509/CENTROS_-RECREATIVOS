from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from lugares.models import Evento, Lugar

from .forms import RegistroForm


def registro(request):
    if request.user.is_authenticated:
        return redirect("lugares:inicio")

    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("lugares:inicio")
    else:
        form = RegistroForm()

    return render(request, "usuarios/registro.html", {"form": form})


@login_required
def mis_sugerencias(request):
    """Lugares y eventos que el usuario ha sugerido, con su estado de revisión."""
    lugares = Lugar.objects.filter(creado_por=request.user).order_by("-fecha_creacion")
    eventos = Evento.objects.filter(creado_por=request.user).order_by("-fecha_inicio")
    return render(
        request,
        "usuarios/mis_sugerencias.html",
        {"lugares": lugares, "eventos": eventos},
    )
