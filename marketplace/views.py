from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from marketplace.serializers import ConsumerRegistrationSerializer

from rest_framework.generics import ListAPIView
from .models import Product
from .serializers import ProductListSerializer
from rest_framework.pagination import PageNumberPagination

from rest_framework import generics, filters
from .models import Product
from .serializers import ProductListSerializer
from rest_framework.pagination import PageNumberPagination

class ConsumerRegistrationView(CreateAPIView):
    serializer_class = ConsumerRegistrationSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"datail": "successfully created consumer"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50

class ProductListView(ListAPIView):
    serializer_class = ProductListSerializer
    pagination_class = ProductPagination

    def get_queryset(self):
        return Product.objects.filter(is_active=True).order_by('-created_at')

class ProductSearchView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    pagination_class = ProductPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

    def get_queryset(self):
        return Product.objects.filter(is_active=True).order_by('-created_at')