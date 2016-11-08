from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .api import DataSourceViewSet, DatabaseViewSet, TagViewSet


router = DefaultRouter()
router.register(r'datasources', DataSourceViewSet, base_name='api-datasources')
router.register(r'databases', DatabaseViewSet, base_name='api-databases')
router.register(r'tags', TagViewSet, base_name='api-tags')

urlpatterns = [
    url(r'^api/v1/', include(router.urls)),
]
