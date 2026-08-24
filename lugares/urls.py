from django.urls import path

from . import views

app_name = "lugares"

urlpatterns = [
    path("", views.mapa, name="mapa"),
    path("sugerir/", views.sugerir, name="sugerir"),
]
