from rest_framework import viewsets, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsPublicationOwner
from .models import DataSource, Database, Tag, Publication
from .serializers import (DataSourceSerializer, DatabaseSerializer,
                          TagSerializer, PublicationSerializer)


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


class PublicationViewSet(viewsets.ModelViewSet):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    permission_classes = (permissions.IsAdminUser, IsPublicationOwner,)
    # Filters
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filter_fields = ('publishable', 'tags', 'creator', 'responsibles',)
    search_fields = ('name',)

    def perform_create(self, serializer):
        if not self.request.user.is_superuser:
            creator = self.request.user
            serializer.save(creator=creator)
        serializer.save()

    def perform_update(self, serializer):
        if not self.request.user.is_superuser:
            creator = self.request.user
            serializer.save(creator=creator)
        serializer.save()
