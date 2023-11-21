from django.contrib import admin
from .models import User, Campo, TipoUsuario, Anuncio, Sesion, Rating, Reserva

# Register your models here.
admin.site.register(User)
admin.site.register(Campo)
admin.site.register(TipoUsuario)
admin.site.register(Anuncio)
admin.site.register(Sesion)
admin.site.register(Rating)
admin.site.register(Reserva)

