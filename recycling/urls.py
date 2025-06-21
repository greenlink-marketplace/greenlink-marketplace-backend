from django.urls import path
from recycling.views import (
    RecyclingLocationListView,
    MaterialReceptionView,
    AvailableMaterialCategoriesView,
)

urlpatterns = [
    path('locations/',
         RecyclingLocationListView.as_view(),
         name='recycling-location-list'),
    path("receive-material/",
         MaterialReceptionView.as_view(),
         name="receive-material"),
    path(
        "available-material-categories/",
        AvailableMaterialCategoriesView.as_view(),
        name="available-material-categories"
    )
]
