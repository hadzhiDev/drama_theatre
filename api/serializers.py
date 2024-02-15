# from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from core.models import News, Photo, PhotoCategory


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'


class PhotoCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoCategory
        fields = '__all__'



