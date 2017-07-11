from django.shortcuts import render
from core.models import *


# Create your views here.

def home(request):
    return render(request, "opendata/home.html")


def categoria(request, tag=''):
    publicaciones = Publication.objects.filter(tags__name=tag)

    return render(
        request,
        "opendata/categoria.html",
        context={
            'categoria': tag,
            'pubs': publicaciones
        }
    )


def busqueda(request):
    return render(request, "opendata/busqueda.html")


def dato(request):
    return render(request, "opendata/dato.html")
