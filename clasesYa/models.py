from django.db import models
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin

# Reemplamos el userManager por uno personalizado
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
    def __str__(self):
        return 'Code: ' + str(self.id) + ' | Nombre: '  + self.nombre
    
class TipoUsuario(models.Model):
    nombre = models.CharField(max_length = 255, blank=True, default='')
    class Meta:
        verbose_name = 'Tipo de usuario'
        verbose_name_plural = 'Tipos de usuarios'
    def __str__(self):
        return 'Code: ' + str(self.id) + ' | Nombre: '  + self.nombre

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

# Nuevo modelo de usuario
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
    
    def __str__(self):
        return self.email

class Reserva(models.Model):
    idAlumno = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='alumno')
    idProfesor = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='profesor')
    fecha = models.DateField(null=True)
    hora = models.TimeField(null=True)
    estado = models.CharField(max_length = 20, blank=True, default='')
    def __str__(self):
        return 'Fecha: ' + str(self.fecha) + ' | ' + str(self.hora) + ' | Profesor: ' + str(self.idProfesor) + ' | Alumno: ' + str(self.idAlumno)


class ChatRoom(models.Model):
    idProfesor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profesorChat')
    idAlumno = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alumnoChat')
    def __str__(self):
        return 'Profesor: ' + str(self.idProfesor) + ' | Alumno: ' + str(self.idAlumno) + ' | Code: ' + str(self.id)
    
class ChatMessage(models.Model):
    idChatRoom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    idUser = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length = 255, blank=True, default='')
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return 'Usuario: ' + str(self.idUser) + ' | Mensaje: ' + str(self.message) + ' | Timestamp: ' + str(self.timestamp)
  