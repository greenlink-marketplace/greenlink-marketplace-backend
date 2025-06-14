from django.urls import path
from recycling.views import RecyclingLocationListView

urlpatterns = [
    path('locations/',
         RecyclingLocationListView.as_view(),
         name='recycling-location-list'),
]
