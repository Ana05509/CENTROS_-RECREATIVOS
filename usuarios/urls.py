from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "usuarios"

urlpatterns = [
    path("registro/", views.registro, name="registro"),
    path("login/", auth_views.LoginView.as_view(template_name="usuarios/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="lugares:mapa"), name="logout"),
    path("mis-sugerencias/", views.mis_sugerencias, name="mis_sugerencias"),
]
