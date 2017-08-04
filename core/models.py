# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pygments.lexers import get_all_lexers
from django.conf import settings
from django.core.exceptions import ValidationError
from .util import truncate_text
from django.db.models import (Model, Manager, CharField, TextField, BooleanField,
                              DateTimeField, PositiveSmallIntegerField,
                              URLField, ManyToManyField, ForeignKey)
from requests import get as http_get, head as http_head
import requests, requests_ftp
from datetime import datetime


class DataSource(Model):
    notes = CharField('notas', unique=True, max_length=255)

    def short_notes(self):
        return truncate_text(self.notes, 100)

    short_notes.short_description = 'notas'

    def __unicode__(self):
        return self.notes

    class Meta:
        verbose_name = 'fuente de datos'
        verbose_name_plural = 'fuentes de datos'


class Database(Model):
    name = CharField('nombre', unique=True, max_length=100)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'base de datos'
        verbose_name_plural = 'bases de datos'


class Tag(Model):
    name = CharField('tag', max_length=100, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'tags'


class Category(Model):
    """
        Main category under which the Publications will be exposed. For example opendata.lacnic.net/datasets/<mounting_point>/<my_publication>
    """
    name = CharField(
        null=False,
        default='N/A',
        max_length=20
    )

    mounting_point = CharField(
        null=False,
        default='N/A',
        max_length=20
    )

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'categoría'
        verbose_name_plural = 'categorías'


class Publication(Model):
    PROGRAMMING_LANGUAGE_CHOICES = sorted(
        [(item[1][0], item[0]) for item in get_all_lexers() if item[1]])
    MINUTES = 'minutos'
    HOURS = 'horas'
    DAYS = 'días'
    WEEKS = 'semanas'
    MONTHS = 'meses'
    YEARS = 'años'
    UPDATE_TYPE_CHOICES = (
        (MINUTES, 'Minuto/s'),
        (HOURS, 'Hora/s'),
        (DAYS, 'Dia/s'),
        (WEEKS, 'Semana/s'),
        (MONTHS, 'Mes/es'),
        (YEARS, 'Año/s'),
    )
    name = CharField('nombre', max_length=100, db_index=True)
    description = TextField('descripción', blank=True, null=True)
    programming_language = CharField('lenguaje de programación',
                                     choices=PROGRAMMING_LANGUAGE_CHOICES,
                                     max_length=30, blank=True, null=True)
    data_sources = ManyToManyField(DataSource, verbose_name='fuentes de datos',
                                   blank=True)
    update_value = PositiveSmallIntegerField(
        'intervalo de actualización',
        blank=True, null=True,
        help_text='Cada cuanto se generan/actualizan los datos')
    update_type = CharField('unidad de intervalo de actualización',
                            max_length=10, choices=UPDATE_TYPE_CHOICES,
                            blank=True, null=True)
    creator = ForeignKey(settings.AUTH_USER_MODEL, verbose_name='creador',
                         related_name='%(class)s_creator')
    responsibles = ManyToManyField(settings.AUTH_USER_MODEL,
                                   verbose_name='responsables',
                                   related_name='%(class)s_responsible')
    databases = ManyToManyField(Database, verbose_name='bases de datos',
                                blank=True)
    server_path = URLField('ruta al servidor', blank=True, null=True)  # Informational only field
    file_path = CharField('ruta a los datos', blank=True, max_length=200)
    file_format = CharField('formato de los datos', blank=True, max_length=4)
    graph_path = CharField('ruta al gráfico', max_length=200, blank=True,
                           null=True)  # Auxiliary field (doesn't contain data)
    publishable = BooleanField('publicable', default=False)
    created = DateTimeField('fecha de creación', default=datetime.now)
    modified = DateTimeField('última modificación', default=datetime.now)
    started = DateTimeField('primera generación de los datos', null=True)
    tags = ManyToManyField(Tag, verbose_name='tags')

    category = ForeignKey(
        Category,
        null=True,
        verbose_name='categoría principal',
        related_name='%(class)s_category'
    )

    def short_description(self):
        return truncate_text(self.description, 50)

    short_description.short_description = 'descripción'

    def clean(self):
        # Business rules
        if self.created and self.modified and self.created > self.modified:
            raise ValidationError(
                {
                    'created': 'La fecha de creación debe ser menor o igual a'
                               ' la fecha de última modificación.'
                })
        if bool(self.update_value) != bool(self.update_type):  # XOR
            raise ValidationError(
                {
                    'update_type': 'Se deben asignar ambos valores de intervalo'
                                   ' de actualización de datos o ninguno de'
                                   ' ellos.'
                })

    @staticmethod
    def guess_protocol(url):
        if 'http://' in url or 'https://' in url:
            return 'http'
        elif 'ftp://' in url:
            return 'ftp'

    def guess_data_protocol(self):
        return Publication.guess_protocol(self.file_path)

    def guess_chart_protocol(self):
        return Publication.guess_protocol(self.graph_path)

    @staticmethod
    def fetch_remote(url):
        if Publication.guess_protocol(url) == 'http':  # HTTP or HTTPS
            response = http_get(url).text
        elif Publication.guess_protocol(url) == 'ftp':
            requests_ftp.monkeypatch_session()
            s = requests.Session()
            response = s.size(url)  # returns a decimal number
        return response

    @staticmethod
    def head_remote(url):
        if Publication.guess_protocol(url) == 'http':  # HTTP or HTTPS
            response = http_head(url)
        elif Publication.guess_protocol(url) == 'ftp':
            requests_ftp.monkeypatch_session()
            s = requests.Session()
            response = s.head(url)  # returns a decimal number
        return response

    def fetch_remote_data(self):
        """
            Fetch the remote data linked to this Publication.
            :return:  None
        """

        if self.file_path:

            if self.guess_data_protocol() == 'http':  # HTTP or HTTPS
                response = http_get(self.file_path).text
            elif self.guess_data_protocol() == 'ftp':
                requests_ftp.monkeypatch_session()
                s = requests.Session()
                response = s.get(self.file_path).text
            else:
                return None

            datas = self.data_set.all().order_by('-timestamp')
            # First Data for this Publication...
            if len(datas) == 0:
                version_minor = '1'
            else:
                version_minor = datas[0].get_version_minor() + 1

            d = Data(
                data=response,
                timestamp=datetime.now()
            )
            d.set_version_minor(version_minor)
            self.data_set.add(
                d,
                bulk=False  # Save automatically
            )

            return d

    def get_data(self):
        return Data.objects.get_most_recent_data(publication=self)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'publicación'
        verbose_name_plural = 'publicaciones'


class DataManager(Manager):
    def get_most_recent_data(self, publication):
        """
        :param category:
        :return:
        """

        datas = Data.objects.filter(publication=publication).order_by('-timestamp')
        if len(datas) > 0:
            return datas[0]
        else:
            return None

    def get_most_recent_datasets(self, category=''):
        """
        :return: list
        The most recent Datas from that category
        """
        return Data.objects.order_by('publication').distinct('publication')  # .filter(publication__category=category)


class Data(Model):
    timestamp = DateTimeField(null=True)
    data = TextField(null=True)
    version = CharField(
        'Version de los datos, en formato Major.minor (mm cambia incrementalmente de forma automática con cada nueva publicación de los datos, MM de misma manera pero cuando cambia la estructura de los datos)',
        null=False,
        default='0.0',
        max_length=20
    )
    publication = ForeignKey(Publication, default=1)

    objects = DataManager()

    def get_version_major(self):
        return int(self.version.split('.')[0])

    def get_version_minor(self):
        return int(self.version.split('.')[1])

    def set_version_major(self, major):
        minor = self.get_version_minor()
        self.version = "%s.%s" % (major, minor)

    def set_version_minor(self, minor):
        major = self.get_version_major()
        self.version = "%s.%s" % (major, minor)
