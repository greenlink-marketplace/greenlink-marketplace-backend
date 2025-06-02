from django.urls import path
from .views import (
    ConsumerRegistrationView,
    ProductListView,
    ProductSearchView,
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
         name='product-search')
]
