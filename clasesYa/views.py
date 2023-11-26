from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from .models import Anuncio, Campo, TipoUsuario, Reserva, ChatRoom, ChatMessage
import calendar
from datetime import datetime
import locale

User = get_user_model()

def loginUser(request):
    if request.method == "POST":
        if loginUsuario(request):
            return redirect('home')
        else:
            return redirect('login')
    else:
        return render(request, "login.html")
    
@login_required
def home(request):
    #Carga del usuario
    user = request.user

    #Carga del calendario
    cal, month, year, month_name = cargarCalendario()

    #Carga de usuarios y chats   
    if user.tipoUsuario.nombre == "Alumno":
        chatRooms = ChatRoom.objects.filter(idAlumno=user.id)
        chatMessages = ChatMessage.objects.filter(idChatRoom__in=chatRooms)
        anuncios = Anuncio.objects.all()
        reservas = Reserva.objects.filter(idAlumno=user.id)

    elif user.tipoUsuario.nombre == "Profesor":
        chatRooms = ChatRoom.objects.filter(idProfesor=user.id)
        chatMessages = ChatMessage.objects.filter(idChatRoom__in=chatRooms)
        anuncios = Anuncio.objects.all()
        reservas = Reserva.objects.filter(idProfesor=user.id)

    #Funcion para la creacion de un anuncio
    if request.method == "POST":
        if 'anuncioForm' in request.POST:
            if registrarAnuncio(request, user):
                return redirect('home', {
                    'user': user, 
                    'anuncios': anuncios,
                    'calendar': cal, 
                    'month': month, 
                    'year': year, 
                    'monthName': month_name, 
                    'chatMessages': chatMessages, 
                    'chatRooms': chatRooms,
                    'reservas': reservas,
                    })
            else:
                return redirect('home', {
                    'user': user, 
                    'anuncios': anuncios, 
                    'calendar': cal, 
                    'month': month, 
                    'year': year, 
                    'monthName': month_name, 
                    'chatMessages': chatMessages, 
                    'chatRooms': chatRooms,
                    'reservas': reservas,
                    })            
        else:
            return redirect('home', {
                'user': user, 
                'anuncios': anuncios, 
                'calendar': cal, 
                'month': month, 
                'year': year, 
                'monthName': month_name, 
                'chatMessages': chatMessages, 
                'chatRooms': chatRooms,
                'reservas': reservas,
                })
    else:
        return render(request, "home.html", {
            'user': user, 
            'anuncios': anuncios, 
            'calendar': cal, 
            'month': month, 
            'year': year, 
            'monthName': month_name, 
            'chatMessages': chatMessages, 
            'chatRooms': chatRooms,
            'reservas': reservas,
            })
    
def registro(request):
    if request.method == 'POST':
        if registrarUsuario(request):
            return redirect('login')
        else:
            return redirect('registro')
    else:
        return render(request, "registro.html")



# Metodos loquisimos
def registrarUsuario(request):
    email = request.POST.get('inputEmail')
    password = request.POST.get('inputPassword')
    tipoUsuario = request.POST.get('selectTipoUsuario')
    tipoUsuarioBd = TipoUsuario.objects.get(id=tipoUsuario)
    try:
        user = User.objects.create_user(email, password, tipoUsuario=tipoUsuarioBd)
        user.save()
        return True
    except:
        return False

def loginUsuario(request):
    email = request.POST.get('inputEmail')
    password = request.POST.get('inputPassword')
    user = authenticate(request, email=email, password=password)
    if user is not None:
        login(request, user)
        return True
    else:
        return False

def test(request):
    return render(request, "test.html")

def logoutUser(request):
    logout(request)
    return redirect('login')

def cargarCalendario():
    today = datetime.today()
    month = today.month
    year = today.year

    #nombre del mes en español
    locale.setlocale(locale.LC_TIME, 'es_ES.utf8')
    month_name = calendar.month_name[month]

    cal = calendar.monthcalendar(year, month)
    return cal, month, year, month_name

def registrarAnuncio(request, user):
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
    try:
        anuncio.save()
        user.anuncio = anuncio
        user.save()
        return True
    except:
        return False
