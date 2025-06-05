from django.urls import path
from marketplace.views import (
    ConsumerRegistrationView,
    ProductListView,
    ProductSearchView,
    ConsumerSavedProductListView,
    ConsumerSavedProductCreateView,
    ConsumerSavedProductDestroyView,
    ProductRetrieveView,
)

urlpatterns = [
    path("register/consumer/",
         ConsumerRegistrationView.as_view(),
         name="consumer-register"),
    path('products/', 
         ProductListView.as_view(), 
         name='product-list'),
    path('products/search/', 
         ProductSearchView.as_view(), 
         name='product-search'),
    path('products/<int:pk>/',
         ProductRetrieveView.as_view(),
         name='product-detail'),
    path('saved-products/list/',
         ConsumerSavedProductListView.as_view(),
         name='saved-products-list'),
    path('saved-products/add/',
         ConsumerSavedProductCreateView.as_view(),
         name='saved-product-create'),
    path('saved-products/delete/<int:pk>/',
         ConsumerSavedProductDestroyView.as_view(),
         name='saved-product-destroy'),
]
