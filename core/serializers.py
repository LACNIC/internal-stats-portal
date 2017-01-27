# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import DataSource, Database, Tag, Publication


class DataSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSource
        fields = ('id', 'notes',)


class DatabaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Database
        fields = ('id', 'name',)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name',)


class PublicationSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(PublicationSerializer, self).__init__(*args, **kwargs)
        request = self.context['request']
        if (not request.user.is_superuser and
                    request.method in ('POST', 'PATCH', 'PUT')):
            self.fields.pop('creator')

    def validate(self, data):
        # Business rules
        created = 'created' in data
        modified = 'modified' in data
        if created and modified:
            if data['created'] > data['modified']:  # POST / PUT
                raise serializers.ValidationError({
                    'created': 'La fecha de creación debe ser menor o igual a'
                               ' la fecha de última modificación.'
                })
        elif created and data['created'] > self.instance.modified:  # PATCH
            raise serializers.ValidationError({
                'created': 'La fecha de creación debe ser menor o igual a la'
                           ' fecha de última modificación.'
            })
        elif modified and self.instance.created > data['modified']:  # PATCH
            raise serializers.ValidationError({
                'created': 'La fecha de creación debe ser menor o igual a la'
                           ' fecha de última modificación.'
            })

        if ('update_value' in data) != ('update_type' in data):  # XOR
            raise serializers.ValidationError({
                'update_type': 'Se deben asignar ambos valores de intervalo'
                               ' de actualización de datos o ninguno de ellos.'
            })
        return data

    class Meta:
        model = Publication
        fields = ('id', 'name', 'description', 'programming_language',
                  'data_sources', 'update_value', 'update_type', 'creator',
                  'responsibles', 'databases', 'server_path', 'file_path', 'graph_path',
                  'publishable', 'created', 'modified', 'started', 'tags',)
