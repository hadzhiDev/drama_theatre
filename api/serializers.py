# from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from core.models import News


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'



