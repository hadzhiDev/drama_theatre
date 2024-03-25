from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from django.conf import settings

from core.models import *


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'


class PhotoCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoCategory
        fields = '__all__'


class PhotoSerializer(serializers.ModelSerializer):
    photo_cat = PhotoCategorySerializer(many=False)

    class Meta:
        model = Photo
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name')


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ('id', 'full_name')


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ('id', 'full_name')


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'


class TicketTypeSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=True)

    class Meta:
        model = TicketType
        fields = ('id', 'price', 'from_row', 'to_row', 'seance', 'tickets')


class PerformanceSeanceSerializer(serializers.ModelSerializer):
    ticket_types = TicketTypeSerializer(many=True, read_only=True)

    class Meta:
        model = PerformanceSeance
        fields = ('id', 'time', 'date', 'ticket_types',)


# class PerformanceDaySerializer(serializers.ModelSerializer):
#     seances = PerformanceSeanceSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = PerformanceDay
#         fields = ('id', 'date', 'seances',)


class RepertoireSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    director = DirectorSerializer(many=False)
    actors = ActorSerializer(many=True)
    # performance_days = PerformanceDaySerializer(many=True, read_only=True)
    seances = PerformanceSeanceSerializer(many=True, read_only=True)

    class Meta:
        model = Repertoire
        fields = '__all__'


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = '__all__'


class HallRowSerializer(serializers.ModelSerializer):
    seats = SeatSerializer(many=True, read_only=True)

    class Meta:
        model = HallRow
        fields = '__all__'


class HallSerializer(serializers.ModelSerializer):
    hall_rows = HallRowSerializer(many=True, read_only=True)

    class Meta:
        model = Hall
        fields = '__all__'

