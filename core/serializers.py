from rest_framework import serializers
from .models import DataSource, Database, Tag


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
