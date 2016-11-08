from rest_framework import viewsets, filters
from .models import DataSource, Database, Tag
from .serializers import DataSourceSerializer, DatabaseSerializer, TagSerializer


class DataSourceViewSet(viewsets.ModelViewSet):
    queryset = DataSource.objects.all()
    serializer_class = DataSourceSerializer
    # Filters
    filter_backends = (filters.SearchFilter,)
    search_fields = ('notes',)


class DatabaseViewSet(viewsets.ModelViewSet):
    queryset = Database.objects.all()
    serializer_class = DatabaseSerializer
    # Filters
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    # Filters
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
