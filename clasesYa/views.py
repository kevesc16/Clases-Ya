from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from .models import Anuncio, Campo, TipoUsuario

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
    
