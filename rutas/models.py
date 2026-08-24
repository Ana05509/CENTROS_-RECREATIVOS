from django.db import models

from lugares.models import Lugar


class TipoTransporte(models.TextChoices):
    VEHICULO = "vehiculo", "Vehículo"
    A_PIE = "a_pie", "A pie"
    BICICLETA = "bicicleta", "Bicicleta"
    BUS = "bus", "Bus"


class Ruta(models.Model):
    """Ruta de acceso hacia un Lugar, trazada como una lista de puntos
    (lat, lng) para dibujarse como polilínea en el mapa."""

    nombre = models.CharField(max_length=200)
    lugar = models.ForeignKey(
        Lugar,
        on_delete=models.CASCADE,
        related_name="rutas",
    )

    punto_partida = models.CharField(
        max_length=200,
        help_text="Ejemplo: Parque Central de La Maná",
    )
    descripcion = models.TextField(blank=True)

    tipo_transporte = models.CharField(
        max_length=20,
        choices=TipoTransporte.choices,
        default=TipoTransporte.VEHICULO,
    )
    distancia_km = models.FloatField(blank=True, null=True)
    tiempo_estimado = models.CharField(
        max_length=50,
        blank=True,
        help_text="Ejemplo: 45 min",
    )

    trazado = models.JSONField(
        help_text="Lista de puntos [[lat, lng], ...] que forman la ruta",
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} → {self.lugar.nombre}"
