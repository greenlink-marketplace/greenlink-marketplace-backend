from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from recycling.models import (
    RecyclingLocation,
    RecyclingManager,
    RecyclableMaterialCategory,
)
from recycling.serializers import (
    RecyclingLocationSerializer,
    RecyclableMaterialReceptionSerializer,
    RecyclableMaterialCategorySerializer,
    ConsumerSummarySerializer,
)
from recycling.services import RecyclableMaterialServices
from marketplace.models import Consumer
from django.contrib.auth import get_user_model

User = get_user_model()

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


class MaterialReceptionView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RecyclableMaterialReceptionSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            recycling_manager_obj = get_object_or_404(RecyclingManager,
                                                      user=request.user)

            recyclable_material_obj = RecyclableMaterialServices.receive(
                recycling_manager_obj=recycling_manager_obj,
                **serializer.validated_data
            )

            return Response(
                {
                    "detail": "Material received successfully.",
                    "recyclable_material_pk": recyclable_material_obj.pk
                },
                status=status.HTTP_201_CREATED
            )
        except Http404 as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class AvailableMaterialCategoriesView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RecyclableMaterialCategorySerializer

    def get_queryset(self):
        user = self.request.user

        # Verify if user is a recycling manager
        try:
            manager = RecyclingManager.objects.get(user=user)
        except RecyclingManager.DoesNotExist:
            raise PermissionDenied(
                "You must be a Recycling Manager to access this resource."
            )

        # Filters categories that have a price for the manager's location
        location = manager.recycling_location
        return RecyclableMaterialCategory.objects.filter(
            materialprice__recycling_location=location
        ).distinct()


class ConsumerSearchView(ListAPIView):
    serializer_class = ConsumerSummarySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = [
        'user__username',
        'cpf'
    ]

    def get_queryset(self):
        user = self.request.user

        # If the user is not a recycling manager, the queryset will be empty,
        #  preventing him from performing any search.
        if user.role != User.UserRole.RECYCLING_MANAGER:
            return Consumer.objects.none()

        return Consumer.objects.select_related('user')
