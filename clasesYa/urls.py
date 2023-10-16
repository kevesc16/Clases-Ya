from django.urls import path
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url='/static/img/favicon.ico')),
    path("", views.login),
    path("login/", views.login),
    path("home/", views.home),
    path("registro/", views.registro),
    path("test/", views.test),
]
