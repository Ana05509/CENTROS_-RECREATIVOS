from django import forms

from .models import Evento, Lugar, Multimedia, TipoMultimedia


class SugerenciaLugarForm(forms.ModelForm):
    class Meta:
        model = Lugar
        fields = [
            "nombre", "categoria", "descripcion", "direccion",
            "latitud", "longitud", "horario", "costo_entrada", "imagen",
        ]
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 3}),
            "latitud": forms.NumberInput(attrs={"step": "any", "placeholder": "Ej. -0.9431"}),
            "longitud": forms.NumberInput(attrs={"step": "any", "placeholder": "Ej. -79.2312"}),
            "horario": forms.TextInput(attrs={"placeholder": "Ej. 08:00 - 18:00"}),
        }


class SugerenciaEventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ["nombre", "lugar", "descripcion", "fecha_inicio", "fecha_fin", "imagen"]
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 3}),
            "fecha_inicio": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "fecha_fin": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["lugar"].queryset = Lugar.objects.filter(aprobado=True).order_by("nombre")


class SugerenciaMultimediaForm(forms.ModelForm):
    class Meta:
        model = Multimedia
        fields = ["lugar", "tipo", "archivo", "url_video", "descripcion"]
        widgets = {
            "descripcion": forms.TextInput(attrs={"placeholder": "Ej. Vista desde el mirador"}),
            "url_video": forms.URLInput(attrs={"placeholder": "https://www.youtube.com/watch?v=..."}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["lugar"].queryset = Lugar.objects.filter(aprobado=True).order_by("nombre")

    def clean(self):
        cleaned = super().clean()
        tipo = cleaned.get("tipo")
        archivo = cleaned.get("archivo")
        url_video = cleaned.get("url_video")

        if tipo == TipoMultimedia.FOTO and not archivo:
            self.add_error("archivo", "Sube una foto.")
        if tipo == TipoMultimedia.VIDEO and not archivo and not url_video:
            self.add_error("url_video", "Sube un archivo de video o pega un link de YouTube.")

        return cleaned
