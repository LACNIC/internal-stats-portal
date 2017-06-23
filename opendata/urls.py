from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from views import home

urlpatterns = [
    url(r'^$', home, name='home')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)