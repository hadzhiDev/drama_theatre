# rom django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet

from api.paginations import SimpleResultPagination
from api.serializers import NewsSerializer, PhotoSerializer, PhotoCategorySerializer
from core.models import News, Photo, PhotoCategory


class NewsViewSet(ModelViewSet):
    queryset = News.objects.all()
    pagination_class = SimpleResultPagination
    serializer_class = NewsSerializer
    lookup_field = 'id'
    search_fields = ['title', 'description', 'content']


class PhotoViewSet(ModelViewSet):
    queryset = Photo.objects.all()
    pagination_class = SimpleResultPagination
    serializer_class = PhotoSerializer
    lookup_field = 'id'
    search_fields = ['photo_cat', 'created_at',]


class PhotoCategoryViewSet(ModelViewSet):
    queryset = PhotoCategory.objects.all()
    pagination_class = SimpleResultPagination
    serializer_class = PhotoCategorySerializer
    lookup_field = 'id'
    search_fields = ['name', 'created_at',]

