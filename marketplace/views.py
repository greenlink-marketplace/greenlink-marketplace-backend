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
from rest_framework.exceptions import ValidationError, APIException
from rest_framework import status
from django.db.utils import IntegrityError
from marketplace.serializers import (
    ConsumerRegistrationSerializer,
    ProductListSerializer,
    ProductRetrieveSerializer,
    ConsumerSavedProductListSerializer,
    ConsumerSavedProductCreateSerializer
)
from marketplace.models import (
    Product,
    ConsumerSavedProduct,
)

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

class NonEmptySearchFilter(SearchFilter):
    def get_search_terms(self, request):
        # Call the original SearchFilter method to get the search terms.
        search_terms = super().get_search_terms(request)

        # If the list of search terms is empty (meaning that
        # the 'search' parameter was not provided or was empty after trim),
        # we raise a ValidationError.
        if not search_terms:
            raise ValidationError(
                {"search": "This field is required."}
            )
        return search_terms

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
