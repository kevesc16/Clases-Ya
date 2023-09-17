from django.urls import path
from . import views

urlpatterns = [
    path("", views.login),
    path("login/", views.login),
    path("home/", views.home),
    path("registro/", views.registro),
    path("perfil/", views.perfil),
]
