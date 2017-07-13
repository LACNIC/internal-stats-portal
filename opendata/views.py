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
    categorias = []
    for p in publicaciones:
        for i in p.tags.all():
            categorias.append(i)

    return render(
        request,
        "opendata/home.html",
        context={
            'pubs' : publicaciones,
            'recent' : recientes,
            'most' : mas_vistas,
            'cat' : set(categorias)
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
    tags = ''
    for tag in publicacion.tags.all():
        if tags == '':
            tags = tags + str(tag)
        else:
            tags = tags + ', ' + str(tag)
    ts_dato = publicacion.get_data().timestamp
    file_name = publicacion.name + '-' + str(ts_dato.date()) + '.' + publicacion.file_format

    return render(
        request,
        "opendata/dato.html",
        context={
            'nombre' : name,
            'pub' : publicacion,
            'tags' : tags,
            'file' : file_name
        }
    )
