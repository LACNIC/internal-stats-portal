from django.shortcuts import render
from core.models import *
from django.http import HttpResponseRedirect
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
            'recent' : recientes[0:4],
            'most' : mas_vistas[0:4],
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


def dato(request, name=''):
    publicacion = Publication.objects.get(name=name)
    tags = []
    for tag in publicacion.tags.all():
        tags.append(tag)
        # if tags == '':
        #     tags = tags + str(tag)
        # else:
        #     tags = tags + ', ' + str(tag)
    ts_dato = publicacion.get_data().timestamp
    file_name = "data/" + publicacion.name.replace(" ", "_").lower() + '-' + str(ts_dato.date()) + '.' + publicacion.file_format
    format = publicacion.file_format

    return render(
        request,
        "opendata/dato.html",
        context={
            'nombre' : name,
            'pub' : publicacion,
            'tags' : tags,
            'file' : file_name,
            'format' : format,
            'ult_alt': ts_dato
        }
    )

def search(request):
    q = request.GET.get('q')
    datos = Publication.objects.filter(name__search=q)
    cats = Tag.objects.filter(name__search=q)

    return render(
        request,
        'opendata/busqueda.html',
        context={
            'datos' : datos,
            'categorias' : cats
        }
    )

def redirect(request):
    """
    :param request:
    :return: HTTP redirect to the static file
    """

    redirect_from = request.path_info
    redirect_to = redirect_from.replace('/redirect/', '/static/')

    filename = redirect_from.split('/')[-1].split('.')[0].split('-')[0]

    pub = None
    for p in Publication.objects.all():
        if filename == p.get_filename():
            pub = p
            break

    red = Redirect(
        redirect_from=redirect_from,
        redirect_to=redirect_to,
        publication=pub
    )
    red.save()

    return HttpResponseRedirect(redirect_to)