from django.db import transaction
from django.contrib.auth import get_user_model
from marketplace.models import Consumer
from recycling.models import (
    RecyclableMaterialCategory,
    MaterialPrice,
    RecyclableMaterial,
    RecyclingManager
)

User = get_user_model()

class RecyclableMaterialServices:

    @classmethod
    @transaction.atomic
    def receive(cls, *,
                material_category_obj: RecyclableMaterialCategory,
                recycling_manager_obj: RecyclingManager,
                name: str,
                description: str,
                quantity_gram: int,
                consumer_obj: Consumer|None = None) -> RecyclableMaterial:
        
        if recycling_manager_obj.user.role != User.UserRole.RECYCLING_MANAGER:
            raise PermissionError(
                "Only recycling managers can receive materials."
            )

        recycling_location = recycling_manager_obj.recycling_location
        if not recycling_location:
            raise ValueError("Manager has no associated recycling location.")

        try:
            price = MaterialPrice.objects.get(
                recycling_location=recycling_location,
                recyclable_material_category=material_category_obj
            )
        except MaterialPrice.DoesNotExist:
            raise ValueError(
                "Price for material category at this location not found."
            )

        credit_cents = 0

        if consumer_obj:
            credit_cents = int(
                price.price_per_kg_cents * (quantity_gram / 1000)
            )
            consumer_obj.green_credit_balance += credit_cents
            consumer_obj.save()

        recyclable_material_obj = RecyclableMaterial.objects.create(
            recycling_location=recycling_location,
            category=material_category_obj,
            consumer=consumer_obj,
            name=name,
            description=description,
            quantity_gram=quantity_gram
        )

        return recyclable_material_obj
