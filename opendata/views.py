from core.models import *
from django.db.models import Count
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.decorators.cache import cache_page
from itertools import chain
from opendata.models import *
import pytz


@cache_page(60 * 15)
def home(request):
    publicaciones = Publication.objects.get_publishable()
    recientes = sorted(publicaciones, reverse=True)
    # for p in publicaciones:
    #     if (datetime.utcnow().replace(tzinfo=pytz.utc) - p.created).days <= 182:
    #         recientes.append(p)

    print Publication.objects.get_publishable().annotate(
        count=Count('visit__publication')
    ).order_by('-count')[:4]

    print Publication.objects.get_publishable().annotate(
        count=Count('redirect__publication')
    ).order_by('-count')[:4]

    mas_visitadas = Publication.objects.get_publishable().annotate(
        count=Count('visit__publication')
    ).annotate(
        count=Count('redirect__publication')
    ).order_by('-count')[:4]

    categorias = []
    for p in publicaciones:
        for i in p.tags.all():
            categorias.append(i)

    return render(
        request,
        "opendata/home.html",
        context={
            'pubs': publicaciones,
            'recent': recientes[0:4],
            'most': mas_visitadas,
            'cat': set(categorias)
        }
    )


def categoria(request, tag=''):
    publicaciones = Publication.objects.get_publishable().filter(tags__name=tag)
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
            'rel': set(related_tags)
        }
    )


def dato(request, name=''):
    """
        :param request: HTTP Request
        :param name: nombre de la Publicacion
        :return:
    """

    publicacion = Publication.objects.get_publishable().get(name=name)

    Visit(
        url=request.path_info,
        publication=publicacion,
        date=datetime.now(),
    ).save()

    tags = []
    for tag in publicacion.tags.all():
        tags.append(tag)

    ts_dato = publicacion.get_data().timestamp
    file_name = "data/" + publicacion.name.replace(" ", "_").lower() + '-' + str(
        ts_dato.date()) + '.' + publicacion.file_format
    format = publicacion.file_format

    return render(
        request,
        "opendata/dato.html",
        context={
            'nombre': name,
            'pub': publicacion,
            'tags': tags,
            'file': file_name,
            'format': format,
            'ult_alt': ts_dato,
            'data_size': len(publicacion.get_data().data)
        }
    )


def search(request):
    q = request.GET.get('q')
    datos = Publication.objects.get_publishable().filter(name__search=q)
    cats = Tag.objects.filter(name__search=q)
    desc = Publication.objects.filter(description__search=q)

    return render(
        request,
        'opendata/busqueda.html',
        context={
            'datos': datos,
            'categorias': cats,
            'descripcion': desc
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
    for p in Publication.objects.get_publishable():
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
