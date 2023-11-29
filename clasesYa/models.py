from django.db import models
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
from django.contrib.auth import get_user_model


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Ingresa un email!')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user
    def create_user(self, email = None, password = None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email = None, password = None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)    
class Campo(models.Model):
    nombre = models.CharField(max_length = 255, blank=True, default='')
    class Meta:
        verbose_name = 'Campo'
        verbose_name_plural = 'Campos'
class TipoUsuario(models.Model):
    nombre = models.CharField(max_length = 255, blank=True, default='')
    class Meta:
        verbose_name = 'Tipo de usuario'
        verbose_name_plural = 'Tipos de usuarios'
class Anuncio(models.Model):
    titulo = models.CharField(max_length = 255, blank=True, default='')
    subTitulo = models.CharField(max_length = 255, blank=True, default='')
    descripcion = models.CharField(max_length = 255, blank=True, default='')
    precio = models.IntegerField(blank=True, default=0)
    campo = models.ForeignKey(Campo, on_delete=models.CASCADE, default=1) 
class Sesion(models.Model):
    duracion = models.IntegerField(blank=True, default=0)
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)
    anuncio = models.ForeignKey(Anuncio, on_delete=models.CASCADE, default=1)
class Rating(models.Model):
    valor = models.IntegerField(blank=True, default=0)
    comentario = models.CharField(max_length = 255, blank=True, default='')
    sesion = models.ForeignKey(Sesion, on_delete=models.CASCADE, default=1)
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(blank = True, default='', unique=True)
    username = models.CharField(max_length = 255, blank=True, default='')
    nombre = models.CharField(max_length = 255, blank=True, default='')
    apellido = models.CharField(max_length = 255, blank=True, default='')
    rut = models.IntegerField(blank=True, default=12345678)
    dv = models.CharField(max_length = 1, blank=True, default='k')
    telefono = models.IntegerField(blank=True, default=12345678)
    creditos = models.IntegerField(blank=True, default=0)
    rating = models.IntegerField(blank=True, default=0)
    anuncio = models.ForeignKey(Anuncio, on_delete=models.CASCADE, blank=True, null=True)
    tipoUsuario = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default = True)
    is_superuser = models.BooleanField(default = False)
    is_staff = models.BooleanField(default = False)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    def get_full_name(self):
        return self.username   
    def get_short_name(self):
        return self.username or self.email.split('@')[0]

class Clase(models.Model):
    nombre = models.CharField(max_length = 255, blank=True, default='')
    descripcion = models.CharField(max_length = 255, blank=True, default='')
    precio = models.IntegerField(blank=True, default=0)
    profesor = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    campo = models.ForeignKey(Campo, on_delete=models.CASCADE, default=1)
    sesion = models.ForeignKey(Sesion, on_delete=models.CASCADE, default=1)
    rating = models.IntegerField(blank=True, default=0)

class Reserva(models.Model):
    idAlumno = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='alumno')
    idProfesor = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='profesor')
    fechaHora = models.DateTimeField(null=True)
    estado = models.CharField(max_length = 20, blank=True, default='')

