from django.db import models
from marketplace.models import Consumer
from django.conf import settings
from django.core.exceptions import ValidationError

class Recycler(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True
    )
    cpf = models.CharField(max_length=14, null=True, blank=True)
    cnpj = models.CharField(max_length=18, null=True, blank=True)
    phone = models.CharField(max_length=14)
    address = models.CharField(max_length=255)

    def clean(self):
        if not self.cpf and not self.cnpj:
            raise ValidationError("Recycler must have at least a CPF or CNPJ.")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class RecyclableMaterialCategory(models.Model):
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class RecyclingLocation(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    contact = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.name


class RecyclingManager(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True
    )
    phone = models.CharField(max_length=14)
    recycling_location = models.ForeignKey(
        RecyclingLocation,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user.get_full_name()} \
            - Manager at {self.recycling_location}"


class RecyclableMaterial(models.Model):
    category = models.ForeignKey(
        RecyclableMaterialCategory,
        on_delete=models.SET_NULL,
        null=True
    )
    consumer = models.ForeignKey(
        Consumer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    recycler = models.ForeignKey(
        Recycler,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    recycling_location = models.ForeignKey(
        RecyclingLocation,
        on_delete=models.SET_NULL,
        null=True
    )
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    quantity_gram = models.PositiveIntegerField(
        help_text="Stored in grams. For example: 12000 = 12kg"
    )
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.quantity_gram/1000}kg)"


class MaterialPrice(models.Model):
    recycling_location = models.ForeignKey(
        RecyclingLocation,
        on_delete=models.CASCADE
    )
    recyclable_material_category = models.ForeignKey(
        RecyclableMaterialCategory,
        on_delete=models.CASCADE
    )
    price_per_kg_cents = models.PositiveIntegerField(
        help_text="Stored in cents. For example: 199 = R$1.99"
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('recycling_location',
                           'recyclable_material_category')

    def __str__(self):
        price = self.price_per_kg_cents / 100
        return (f"Price for {self.recyclable_material_category.name} "
                f"at {self.recycling_location.name}: R${price:.2f}/kg")
