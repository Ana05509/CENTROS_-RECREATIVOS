from django.urls import path

from . import views

app_name = "lugares"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("mapa/", views.mapa, name="mapa"),
    path("sugerir/", views.sugerir, name="sugerir"),
]
