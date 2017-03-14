from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .api import (DataSourceViewSet, DatabaseViewSet, TagViewSet,
                  PublicationViewSet, DataViewSet)

router = DefaultRouter()
router.register(r'datasources', DataSourceViewSet, base_name='api-datasources')
router.register(r'databases', DatabaseViewSet, base_name='api-databases')
router.register(r'tags', TagViewSet, base_name='api-tags')
router.register(r'publications', PublicationViewSet,
                base_name='api-publications')
router.register(r'datas', DataViewSet,
                base_name='api-datas')

urlpatterns = [
    url(r'', include(router.urls)),
]
