from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request, "login.html")

def home(request):
    return render(request, "home.html")

def registro(request):
    return render(request, "registro.html")

def perfil(request):
    return render(request, "perfil.html")

def test(request):
    return render(request, "test.html")