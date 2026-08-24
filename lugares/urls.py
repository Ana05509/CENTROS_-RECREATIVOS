from django.urls import path

from . import views

app_name = "lugares"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("mapa/", views.mapa, name="mapa"),
    path("lugares/", views.lista_lugares, name="lista"),
    path("sugerir/", views.sugerir, name="sugerir"),
    path("lugar/<int:lugar_id>/", views.detalle_lugar, name="detalle"),
]
