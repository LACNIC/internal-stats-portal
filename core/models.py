# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pygments.lexers import get_all_lexers
from django.conf import settings
from django.core.exceptions import ValidationError
from .util import truncate_text
from django.db.models import (Model, CharField, TextField, BooleanField,
                              DateTimeField, PositiveSmallIntegerField,
                              URLField, ManyToManyField, ForeignKey)


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


class Publication(Model):
    PROGRAMMING_LANGUAGE_CHOICES = sorted(
        [(item[1][0], item[0]) for item in get_all_lexers() if item[1]])
    MINUTES = 'mins'
    HOURS = 'hours'
    DAYS = 'days'
    MONTHS = 'months'
    YEARS = 'years'
    UPDATE_TYPE_CHOICES = (
        (MINUTES, 'Minuto/s'),
        (HOURS, 'Hora/s'),
        (DAYS, 'Dia/s'),
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
    server_path = URLField('ruta al servidor', blank=True, null=True)
    file_path = CharField('ruta a los datos', max_length=200)
    graph_path = CharField('ruta al gráfico', max_length=200)
    publishable = BooleanField('publicable', default=False)
    created = DateTimeField('fecha de creación')
    modified = DateTimeField('última modificación')
    started = DateTimeField('primera generación de los datos')
    tags = ManyToManyField(Tag, verbose_name='tags')

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

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'publicación'
        verbose_name_plural = 'publicaciones'
