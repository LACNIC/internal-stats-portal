from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from views import home, categoria, busqueda, dato

urlpatterns = [
    url(r'^$', home, name='home'),
url(r'^categoria/$', categoria, name='categoria'),
url(r'^busqueda/$', busqueda, name='busqueda'),
url(r'^dato/$', dato, name='dato')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)