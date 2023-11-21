from django.urls import path
from django.views.generic.base import RedirectView
from . import views
from .views import reservar_clase

urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url='/static/img/favicon.ico')),
    path("", views.loginUser),
    path("login/", views.loginUser, name='login'), 
    path("logout/", views.logoutUser, name='logout'),
    path("home/", views.home, name='home'),
    path("registro/", views.registro, name='registro'),
    path("test/", views.test),
    path('reservar_clase/<int:clase_id>/', reservar_clase, name='reservar_clase'),
]

