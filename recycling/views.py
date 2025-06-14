import django_filters
from recycling.models import RecyclingLocation
from rest_framework.generics import ListAPIView
from recycling.models import RecyclingLocation
from recycling.serializers import RecyclingLocationSerializer
from django_filters.rest_framework import DjangoFilterBackend


class RecyclingLocationFilter(django_filters.FilterSet):
    latitude_min = django_filters.NumberFilter(field_name="latitude",
                                               lookup_expr='gte',
                                               required=True)
    latitude_max = django_filters.NumberFilter(field_name="latitude",
                                               lookup_expr='lte',
                                               required=True)
    longitude_min = django_filters.NumberFilter(field_name="longitude",
                                                lookup_expr='gte',
                                                required=True)
    longitude_max = django_filters.NumberFilter(field_name="longitude",
                                                lookup_expr='lte',
                                                required=True)

    class Meta:
        model = RecyclingLocation
        fields = []


class RecyclingLocationListView(ListAPIView):
    queryset = RecyclingLocation.objects.all()
    serializer_class = RecyclingLocationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecyclingLocationFilter
