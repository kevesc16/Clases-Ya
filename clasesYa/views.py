from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from .models import Anuncio, Campo, TipoUsuario, Reserva, ChatRoom, ChatMessage
from django.http import JsonResponse

import calendar
from datetime import datetime
import locale
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated



User = get_user_model()


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

    #Carga de reservas, usuarios y chats
    user = request.user
    anuncios = Anuncio.objects.all()

    if user.tipoUsuario.nombre == "Alumno":
        reservas = Reserva.objects.filter(idAlumno=user.id)
        profesor_ids = reservas.values_list('idProfesor', flat=True)
        usuarios = User.objects.filter(id__in=profesor_ids)
        chatRooms = ChatRoom.objects.filter(idAlumno=user.id)
        chatMessages = ChatMessage.objects.filter(idChatRoom__in=chatRooms)

    elif user.tipoUsuario.nombre == "Profesor":
        reservas = Reserva.objects.filter(idProfesor=user.id)
        alumno_ids = reservas.values_list('idAlumno', flat=True)
        usuarios = User.objects.filter(id__in=alumno_ids)
        chatRooms = ChatRoom.objects.filter(idProfesor=user.id)
        chatMessages = ChatMessage.objects.filter(idChatRoom__in=chatRooms)


    #Funciones para el calendario
    today = datetime.today()
    month = today.month
    year = today.year

    #nombre del mes en español
    locale.setlocale(locale.LC_TIME, 'es_ES.utf8')
    month_name = calendar.month_name[month]

    cal = calendar.monthcalendar(year, month)

    #Funcion para la creacion de un anuncio
    if request.method == "POST":
        if 'anuncioForm' in request.POST:
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
            print(f"anuncio: {anuncio}, user: {user}")
            user.anuncio = anuncio
            user.save()
            
            return redirect('home', {'user': user, 'anuncios': anuncios, 'calendar': cal, 'month': month, 'year': year, 'monthName': month_name, 'reservas': reservas, 'usuarios': usuarios, 'chatMessages': chatMessages, 'chatRooms': chatRooms})
        else:
            return redirect('home', {'user': user, 'anuncios': anuncios, 'calendar': cal, 'month': month, 'year': year, 'monthName': month_name, 'reservas': reservas, 'usuarios': usuarios, 'chatMessages': chatMessages, 'chatRooms': chatRooms})
    else:

        return render(request, "home.html", {'user': user, 'anuncios': anuncios, 'calendar': cal, 'month': month, 'year': year, 'monthName': month_name, 'reservas': reservas, 'usuarios': usuarios, 'chatMessages': chatMessages, 'chatRooms': chatRooms})

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
    

@csrf_exempt
def sendMessage(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        idUser = request.user
        idChatRoom = request.POST.get('idChatRoom')
        timestamp = datetime.now()
        chatMessage = ChatMessage(message=message, idUser=idUser, idChatRoom=idChatRoom, timestamp=timestamp)
        chatMessage.save()
        return JsonResponse({'status': 'success', 'message': 'Mensaje enviado'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Error al enviar el mensaje'})


       

    
    #idChatRoom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    #idUser = models.ForeignKey(User, on_delete=models.CASCADE)
    #message = models.CharField(max_length = 255, blank=True, default='')
    #timestamp = models.DateTimeField(auto_now_add=True)