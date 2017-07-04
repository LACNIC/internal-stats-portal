from django.shortcuts import render


# Create your views here.

def home(request):
    return render(request, "opendata/home.html")

def categoria(request):
    return render(request, "opendata/categoria.html")

def busqueda(request):
    return render(request, "opendata/busqueda.html")

def dato(request):
    return render(request, "opendata/dato.html")