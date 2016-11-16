from rest_framework import viewsets, filters
from django.contrib.auth import get_user_model
from .serializers import UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    # Filters
    filter_backends = (filters.SearchFilter,)
    search_fields = ('id', 'username', 'first_name', 'last_name', 'email',)
