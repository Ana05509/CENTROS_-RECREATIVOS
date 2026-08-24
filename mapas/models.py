from django.db import models


class TipoPunto(models.TextChoices):
    RECURSO_NATURAL = "recurso_natural", "Recurso natural"
    INFRAESTRUCTURA = "infraestructura", "Infraestructura"


class PuntoInteres(models.Model):
    """Elementos del mapa que no son centros recreativos: ríos, montañas,
    puentes, vías, hospitales, etc. Los centros recreativos viven en
    lugares.Lugar."""

    nombre = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=TipoPunto.choices)
    subtipo = models.CharField(
        max_length=100,
        blank=True,
        help_text="Ejemplo: Río, Puente, Vía, Hospital, Montaña",
    )
    descripcion = models.TextField(blank=True)

    latitud = models.FloatField()
    longitud = models.FloatField()

    icono = models.CharField(
        max_length=50,
        blank=True,
        help_text="Identificador del icono a usar en el mapa (opcional)",
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Punto de interés"
        verbose_name_plural = "Puntos de interés"

    def __str__(self):
        return self.nombre
