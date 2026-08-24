from django import template

from lugares.models import Evento, Lugar, Multimedia

register = template.Library()


@register.inclusion_tag("admin/_panel_pendientes.html")
def panel_pendientes():
    """Conteo real de lugares, eventos y fotos/videos sugeridos por el
    público que todavía no han sido revisados (aprobado=False)."""
    return {
        "lugares_pendientes": Lugar.objects.filter(aprobado=False).count(),
        "eventos_pendientes": Evento.objects.filter(aprobado=False).count(),
        "multimedia_pendientes": Multimedia.objects.filter(aprobado=False).count(),
    }
