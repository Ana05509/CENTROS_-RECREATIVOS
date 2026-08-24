from django import forms

from .models import Evento, Lugar


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
