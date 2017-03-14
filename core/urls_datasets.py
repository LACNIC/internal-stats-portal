from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .api import DatasetsList
from .models import Data

router = DefaultRouter()

# categories = set([data.publication.category.mounting_point for data in Data.objects.get_most_recent_datasets()])

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'(?P<category>\w+)/', DatasetsList.as_view()),
]
