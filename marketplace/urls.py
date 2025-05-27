from django.urls import path
from .views import ConsumerRegistrationView

urlpatterns = [
    path("register/consumer/",
         ConsumerRegistrationView.as_view(),
         name="consumer-register"),
]
