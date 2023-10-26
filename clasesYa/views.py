from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login

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
    return render(request, "home.html")

def test(request):
    return render(request, "test.html")

def registro(request):
    if request.method == 'POST':
        email = request.POST.get('inputEmail')
        password = request.POST.get('inputPassword')
        tipoUsuario = request.POST.get('selectTipoUsuario')
        try:
            user = User.objects.create_user(email, password)
            user.TipoUsuario = tipoUsuario
            user.save()
            return redirect('login')
        except:
            return render(request, "registro.html")
    else:
        return render(request, "registro.html")
    
