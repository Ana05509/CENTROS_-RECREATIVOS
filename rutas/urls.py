from django.urls import path

from . import views

app_name = "rutas"

urlpatterns = [
    path("", views.lista, name="lista"),
]
