from django.urls import path
from recycling.views import (
    RecyclingLocationListView,
    MaterialReceptionView
)

urlpatterns = [
    path('locations/',
         RecyclingLocationListView.as_view(),
         name='recycling-location-list'),
    path("receive-material/",
         MaterialReceptionView.as_view(),
         name="receive-material"),
]
