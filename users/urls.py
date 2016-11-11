from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .api import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, base_name='api-users')

urlpatterns = [
    url(r'^api/v1/', include(router.urls)),
]
