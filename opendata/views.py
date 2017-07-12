from django.shortcuts import render
from core.models import *
import pytz


# Create your views here.

def home(request):
    publicaciones = Publication.objects.all()
    recientes = []
    for p in publicaciones:
        if (datetime.utcnow().replace(tzinfo=pytz.utc) - p.created).days <= 182:
            recientes.append(p)
    mas_vistas = []
    for p in publicaciones:
        if p.programming_language == "python":
            mas_vistas.append(p)

    return render(
        request,
        "opendata/home.html",
        context={
            'pubs' : publicaciones,
            'recent' : recientes,
            'most' : mas_vistas
        }
    )


def categoria(request, tag=''):
    publicaciones = Publication.objects.filter(tags__name=tag)
    related_tags = []
    for p in publicaciones:
        for t in p.tags.all():
            if str(t) != str(tag):
                related_tags.append(t)


    return render(
        request,
        "opendata/categoria.html",
        context={
            'categoria': tag,
            'pubs': publicaciones,
            'rel' : set(related_tags)
        }
    )


def busqueda(request):
    return render(request, "opendata/busqueda.html")


def dato(request, name=''):
    publicacion = Publication.objects.get(name=name)
    cant_tags = len(publicacion.tags.all())

    return render(
        request,
        "opendata/dato.html",
        context={
            'nombre': name,
            'pub': publicacion,
            'n_tags': cant_tags+1
        }
    )
