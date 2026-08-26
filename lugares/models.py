import re

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models

# Extensiones permitidas para Multimedia.archivo y tamaño máximo. Sin esto,
# el campo aceptaría CUALQUIER archivo (ejecutables, HTML, etc.) desde el
# formulario público sin cuenta, y quedaría servido públicamente bajo el
# dominio del sitio.
EXTENSIONES_MULTIMEDIA_PERMITIDAS = ["jpg", "jpeg", "png", "gif", "webp", "mp4", "webm", "mov"]
TAMANO_MAXIMO_MULTIMEDIA_MB = 25


def validar_tamano_multimedia(archivo):
    limite = TAMANO_MAXIMO_MULTIMEDIA_MB * 1024 * 1024
    if archivo.size > limite:
        raise ValidationError(f"El archivo no puede pesar más de {TAMANO_MAXIMO_MULTIMEDIA_MB} MB.")


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Lugar(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    direccion = models.CharField(max_length=255)

    parroquia = models.CharField(
        max_length=100,
        blank=True,
        help_text="Ejemplo: La Maná, Guasaganda, Pucayacu, El Carmen, El Triunfo",
    )

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

    aprobado = models.BooleanField(
        default=True,
        help_text="Los lugares sugeridos por el público quedan sin aprobar "
                   "hasta que el admin los revisa; no aparecen en el mapa "
                   "público hasta entonces."
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

    creado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    aprobado = models.BooleanField(
        default=True,
        help_text="Los eventos sugeridos por el público quedan sin aprobar "
                   "hasta que el admin los revisa."
    )

    def __str__(self):
        return self.nombre


class TipoMultimedia(models.TextChoices):
    FOTO = "foto", "Foto"
    VIDEO = "video", "Video"


class Multimedia(models.Model):
    """Foto o video de la galería de un Lugar. Un lugar puede tener
    varias fotos y varios videos (a diferencia de Lugar.imagen, que es
    una sola imagen de portada)."""

    lugar = models.ForeignKey(Lugar, on_delete=models.CASCADE, related_name="multimedia")
    tipo = models.CharField(max_length=10, choices=TipoMultimedia.choices)

    archivo = models.FileField(
        upload_to="lugares/multimedia/",
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=EXTENSIONES_MULTIMEDIA_PERMITIDAS),
            validar_tamano_multimedia,
        ],
        help_text=(
            "Foto (jpg, png, gif, webp) o video (mp4, webm, mov), máx. "
            f"{TAMANO_MAXIMO_MULTIMEDIA_MB} MB. O usa un link de YouTube."
        ),
    )
    url_video = models.URLField(
        blank=True,
        help_text="Link de YouTube (opcional si subes un archivo de video).",
    )
    descripcion = models.CharField(max_length=200, blank=True)

    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    aprobado = models.BooleanField(
        default=True,
        help_text="Las fotos/videos sugeridos por el público quedan sin "
                   "aprobar hasta que el admin los revisa."
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    _RE_YOUTUBE = re.compile(r"(?:youtube\.com/(?:watch\?v=|embed/|shorts/)|youtu\.be/)([\w-]{11})")

    class Meta:
        verbose_name = "Foto o video"
        verbose_name_plural = "Fotos y videos"
        ordering = ["-fecha_creacion"]

    def __str__(self):
        return f"{self.get_tipo_display()} de {self.lugar.nombre}"

    @property
    def youtube_embed_url(self):
        """URL de embed si url_video es un link de YouTube reconocible, o None."""
        if not self.url_video:
            return None
        match = self._RE_YOUTUBE.search(self.url_video)
        return f"https://www.youtube.com/embed/{match.group(1)}" if match else None

    def clean(self):
        if self.tipo == TipoMultimedia.FOTO and not self.archivo:
            raise ValidationError("Sube una foto.")
        if self.tipo == TipoMultimedia.VIDEO and not self.archivo and not self.url_video:
            raise ValidationError("Sube un archivo de video o pega un link de YouTube.")