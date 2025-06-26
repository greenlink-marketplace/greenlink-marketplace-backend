from django.db import transaction
from django.utils.crypto import get_random_string
from marketplace.models import (
    Consumer,
    Coupon,
    Product,
)

class CouponServices:

    @classmethod
    @transaction.atomic
    def generate(cls,
                 consumer_obj: Consumer,
                 green_credit_amount: int,
                 product_obj: Product) -> Coupon:
        # Check if the consumer has sufficient credits
        if consumer_obj.green_credit_balance < green_credit_amount:
            raise ValueError("Insufficient green credits balance.")

        # Calculates the value of the cents discount
        discount_value_cents = green_credit_amount  # 1 credit = 1 cent

        # Business Rules: Discount between 5% and 20% of the value of the product
        min_discount = int(product_obj.price_cents * 0.05)
        max_discount = int(product_obj.price_cents * 0.20)

        if discount_value_cents < min_discount:
            raise ValueError(
                f"The minimum discount value is {min_discount} cents."
            )
        if discount_value_cents > max_discount:
            raise ValueError(
                f"The maximum discount value is {max_discount} cents."
            )
        
        # Generates single code for the coupon
        coupon_code = get_random_string(10).upper()

        # Debit consumer green credits
        consumer_obj.green_credit_balance -= green_credit_amount
        consumer_obj.save()

        # Create the coupon
        coupon = Coupon.objects.create(
            consumer=consumer_obj,
            coupon_code=coupon_code,
            discount_value_cents=discount_value_cents
        )

        return coupon
