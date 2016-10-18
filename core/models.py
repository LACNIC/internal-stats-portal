# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.db.models import Model, CharField, TextField, BooleanField, \
    DateTimeField, PositiveIntegerField, PositiveSmallIntegerField, URLField, \
    OneToOneField, ManyToManyField, CASCADE
from .util import truncate_text


class Responsible(Model):
    user = OneToOneField(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    comments = TextField('comentarios', blank=True, null=True)

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name = 'responsable'
        verbose_name_plural = 'responsables'


class DataSource(Model):
    notes = TextField('notas', blank=True, null=True)

    @property
    def short_notes(self):
        return truncate_text(self.notes, 100)

    def __unicode__(self):
        return self.notes

    class Meta:
        verbose_name = 'fuente de datos'
        verbose_name_plural = 'fuentes de datos'


class Database(Model):
    name = CharField('nombre', max_length=100)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'base de datos'
        verbose_name_plural = 'bases de datos'


class Publication(Model):
    MINUTOS = 1
    HORAS = 2
    DIAS = 3
    MESES = 4
    ANOS = 5
    UPDATE_TYPE_CHOICES = (
        (MINUTOS, 'Minuto/s'),
        (HORAS, 'Hora/s'),
        (DIAS, 'Dia/s'),
        (MESES, 'Mes/es'),
        (ANOS, 'Año/s'),
    )
    name = CharField('nombre', max_length=100, db_index=True)
    description = TextField('descripción', blank=True, null=True)
    # FALTA - Lenguaje de programación usado para recolectar los datos.
    data_sources = ManyToManyField(DataSource, verbose_name='fuentes de datos',
                                   blank=True)
    update_value = PositiveIntegerField('valor de actualización de datos',
                                        blank=True,
                                        null=True)
    update_type = PositiveSmallIntegerField(
        'tipo de valor de actualización de datos', choices=UPDATE_TYPE_CHOICES,
        blank=True, null=True)
    creator = OneToOneField(settings.AUTH_USER_MODEL, verbose_name='creador')
    responsibles = ManyToManyField(Responsible, verbose_name='responsables')
    databases = ManyToManyField(Database, verbose_name='bases de datos',
                                blank=True)
    server_path = URLField('ruta al servidor', blank=True, null=True)
    file_path = CharField('ruta a los datos', max_length=200)
    publishable = BooleanField('publicable', default=False)
    created = DateTimeField('fecha de creación')
    last_modified = DateTimeField('última modificación')
    # FALTA - Tags

    @property
    def short_description(self):
        return truncate_text(self.description, 50)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'publicación'
        verbose_name_plural = 'publicaciones'
