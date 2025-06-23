from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    DestroyAPIView,
    RetrieveAPIView,
)
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
) 
from rest_framework.exceptions import (
    ValidationError,
    APIException,
    PermissionDenied,
)
from rest_framework import status
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from marketplace.serializers import (
    ConsumerRegistrationSerializer,
    ProductListSerializer,
    ProductRetrieveSerializer,
    ConsumerSavedProductListSerializer,
    ConsumerSavedProductCreateSerializer,
    ProductCreateSerializer,
)
from marketplace.models import (
    Product,
    ConsumerSavedProduct,
)
from common.filters import NonEmptySearchFilter

class ConsumerRegistrationView(CreateAPIView):
    serializer_class = ConsumerRegistrationSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"datail": "successfully created consumer"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductPagination(PageNumberPagination):
    page_size = 60
    page_size_query_param = None
    max_page_size = None

class ProductListView(ListAPIView):
    serializer_class = ProductListSerializer
    pagination_class = ProductPagination

    def get_queryset(self):
        return Product.objects.filter(is_active=True).order_by('-created_at')

class ProductSearchView(ListAPIView):
    serializer_class = ProductListSerializer
    pagination_class = ProductPagination
    filter_backends = [NonEmptySearchFilter]
    search_fields = ['name', 'description']

    def get_queryset(self):
        return Product.objects.filter(is_active=True).order_by('-created_at')

class ProductRetrieveView(RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductRetrieveSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ConsumerSavedProductListView(ListAPIView):
    serializer_class = ConsumerSavedProductListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ConsumerSavedProduct.objects.filter(
            consumer__user=self.request.user
        )

class ConsumerSavedProductCreateView(CreateAPIView):
    queryset = ConsumerSavedProduct.objects.all()
    serializer_class = ConsumerSavedProductCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        try:
            serializer.save(consumer=self.request.user.consumer)
        except IntegrityError:
            raise ValidationError({"detail": "This product has already been saved by this consumer."})
        except Exception:
            raise APIException("An unexpected error occurred while saving the product.")

class ConsumerSavedProductDestroyView(DestroyAPIView):
    queryset = ConsumerSavedProduct.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = "product"
    lookup_url_kwarg = "product_id"

    def get_queryset(self):
        return self.queryset.filter(consumer=self.request.user.consumer)

class ProductCreateView(CreateAPIView):
    serializer_class = ProductCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        # Obtains the configured user model
        User = get_user_model()

        # Checks if the user is of the role 'COMPANY'
        if not user.role == User.UserRole.COMPANY:
            raise PermissionDenied("Apenas empresas podem criar produtos.")

        # Associates the product with the authenticated user company
        serializer.save(company=user.company)
