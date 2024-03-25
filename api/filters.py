from django_filters import rest_framework as filters

from core.models import Repertoire


class RepertoireFilter(filters.FilterSet):
    created_at = filters.DateRangeFilter()

    class Meta:
        model = Repertoire
        fields = ['genres', 'director', ]