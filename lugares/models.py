from django.db import models
from django.contrib.auth.models import User


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Lugar(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    direccion = models.CharField(max_length=255)

    latitud = models.FloatField()
    longitud = models.FloatField()

    horario = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Ejemplo: 08:00 - 18:00"
    )

    costo_entrada = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0.00,
        help_text="Costo en dólares"
    )

    imagen = models.ImageField(
        upload_to='lugares/',
        blank=True,
        null=True
    )

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE
    )

    creado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Evento(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()

    lugar = models.ForeignKey(
        Lugar,
        on_delete=models.CASCADE
    )

    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()

    imagen = models.ImageField(
        upload_to='eventos/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.nombre