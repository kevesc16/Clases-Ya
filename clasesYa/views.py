from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from .models import Anuncio, Campo, TipoUsuario, Reserva, ChatRoom, ChatMessage
from django.http import JsonResponse
import calendar
from datetime import datetime
import locale
from django.utils import timezone

User = get_user_model()

@login_required
def videollamada(request):
    return render(request, "videollamada.html", { 'name': request.user.email })

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
                return render(request, 'home.html', {
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
                return render(request, 'home.html', {
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
        elif 'updateAnuncio' in request.POST:
            user = request.user
            anuncio_id = request.POST.get('updateAnuncio')
            anuncio = Anuncio.objects.get(id=anuncio_id)
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
            return render(request, 'home.html', {
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
        elif 'entrarVideo' in request.POST:
            inputUrl = request.POST['inputUrl']
            return redirect("/videollamada?roomID=" + inputUrl)
        if 'reservarClase' in request.POST:
            anuncioId = request.POST.get('anuncio')
            alumnoId = request.POST.get('idAlumno')
            alumno = User.objects.get(id=alumnoId)
            profesorId = User.objects.get(anuncio=anuncioId)
            nuevaReserva = Reserva(idAlumno=alumno, idProfesor=profesorId)
            nuevaReserva.save()
            return render(request, 'home.html', {
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
            return render(request, 'home.html', {
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
        return render(request, 'home.html', {
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

def get_messages(request, room_id):
    messages = ChatMessage.objects.filter(idChatRoom=room_id).select_related('idUser')
    messages_list = []
    for msg in messages:
        formatted_time = timezone.localtime(msg.timestamp).strftime('%H:%M')
        message_dict = {'id': msg.id, 'idChatRoom': msg.idChatRoom.id, 'idUser': msg.idUser.email, 'message': msg.message, 'timestamp': formatted_time}
        messages_list.append(message_dict)
    return JsonResponse(messages_list, safe=False)