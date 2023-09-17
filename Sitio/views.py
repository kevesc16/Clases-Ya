from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, "home.html")

def login(request):
    return render(request, "login.html")

def registro(request):
    return render(request, "registro.html")

def perfil(request):
    return render(request, "perfil.html")