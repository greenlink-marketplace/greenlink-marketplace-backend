from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from recycling.models import RecyclingLocation

class User(AbstractUser):
    class UserRole(models.TextChoices):
        CONSUMER = "consumer", "Consumer"
        COMPANY = "company", "Company"
        RECYCLER = "recycler", "Recycler"
        RECYCLING_MANAGER = "recycling_manager", "Recycling Manager"
        GENERAL_ADMIN = "general_admin", "General Administrator"

    created_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices
    )
