# rom django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet

from api.paginations import SimpleResultPagination
from api.serializers import NewsSerializer
from core.models import News


class NewsViewSet(ModelViewSet):
    queryset = News.objects.all()
    pagination_class = SimpleResultPagination
    serializer_class = NewsSerializer
    lookup_field = 'id'
    search_fields = ['title', 'description', 'content']

