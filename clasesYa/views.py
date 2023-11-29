import datetime
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from .models import Anuncio, Campo, TipoUsuario, Clase, Sesion, Reserva, User

# Create your views here.
def loginUser(request):
    if request.method == "POST":
        email = request.POST.get('inputEmail')
        password = request.POST.get('inputPassword')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('login')
    else:
        return render(request, "login.html")
    
def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    if request.method == "POST":
        if 'anuncioForm' in request.POST:
            # Lógica para la creación de un nuevo anuncio
            titulo = request.POST.get('inputTitulo')
            subTitulo = request.POST.get('inputSubTitulo')
            descripcion = request.POST.get('inputDescripcion')
            precio = request.POST.get('inputPrecio')
            campo = request.POST.get('inputCampo')
            
            campoReview = Campo.objects.filter(nombre=campo)
            if len(campoReview) == 0:
                nuevoCampo = Campo(nombre=campo)
                nuevoCampo.save()
                campo = nuevoCampo
            else:
                campo = campoReview[0]            
            anuncio = Anuncio(titulo=titulo, subTitulo=subTitulo, descripcion=descripcion, precio=precio, campo=campo)
            user = request.user
            anuncio.save()
            user.anuncio = anuncio
            user.save()
            return redirect('home')
        elif 'updateAnuncio' in request.POST:
            # Lógica para la actualización de un anuncio existente
            user = request.user
            anuncio_id = request.POST.get('updateAnuncio')
            anuncio = Anuncio.objects.get(id=anuncio_id)
            # Actualiza los campos del anuncio con los nuevos valores del formulario
            anuncio.titulo = request.POST.get('inputTitulo')
            anuncio.subTitulo = request.POST.get('inputSubTitulo')
            anuncio.descripcion = request.POST.get('inputDescripcion')
            anuncio.precio = request.POST.get('inputPrecio')
            campo = request.POST.get('inputCampo')
            campoReview = Campo.objects.filter(nombre=campo)

            if len(campoReview) == 0:
                nuevoCampo = Campo(nombre=campo)
                nuevoCampo.save()
                anuncio.campo = nuevoCampo
            else:
                anuncio.campo = campoReview[0]

            anuncio.save()
        if 'reservarClase' in request.POST:
            # Lógica para la reserva de una clase
            anuncioId = request.POST.get('anuncio')
            alumnoId = request.POST.get('idAlumno')
            alumno = User.objects.get(id=alumnoId)
            profesorId = User.objects.get(anuncio=anuncioId)
            nuevaReserva = Reserva(idAlumno=alumno, idProfesor=profesorId)
            nuevaReserva.save()
            return redirect('home')

        else:
            return redirect('home')
    else:
        user = request.user
        anuncios = Anuncio.objects.all()
        return render(request, "home.html", {'user': user, 'anuncios': anuncios})

def test(request):
    return render(request, "test.html")

def registro(request):
    if request.method == 'POST':
        email = request.POST.get('inputEmail')
        password = request.POST.get('inputPassword')
        tipoUsuario = request.POST.get('selectTipoUsuario')
        tipoUsuarioBd = TipoUsuario.objects.get(id=tipoUsuario)
        print(f"email: {email}, password: {password}, tipoUsuario: {tipoUsuario}, tipoUsuarioBd: {tipoUsuarioBd}")
        try:
            user = User.objects.create_user(email, password, tipoUsuario=tipoUsuarioBd)
            user.save()
            return redirect('login')
        except:
            return render(request, "registro.html")
    else:
        return render(request, "registro.html")

