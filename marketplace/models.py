from django.db import models
from django.conf import settings

class Consumer(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True
    )
    
    cpf = models.CharField(max_length=14, unique=True)
    phone = models.CharField(max_length=14)
    address = models.CharField(max_length=255)
    green_credit_balance = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.get_full_name()} (CPF: {self.cpf})"


class Company(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True
    )
    cnpj = models.CharField(max_length=18, unique=True)
    phone = models.CharField(max_length=14)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username


class ProductCategory(models.Model):
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} (pk: {self.pk})"


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    price_cents = models.PositiveIntegerField(
        help_text="Stored in cents. For example: 199 = R$1.99"
    )
    quantity = models.PositiveIntegerField()
    purchase_contact = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products_images/',
                              null=True,
                              blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_sustainable = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ConsumerSavedProduct(models.Model):
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # avoid saving the same product multiple times
        unique_together = ('consumer', 'product')

    def __str__(self):
        return (
            f"{self.consumer} saved {self.product} "
            f"on {self.saved_at.strftime('%Y-%m-%d')}"
        )


class Coupon(models.Model):
    consumer = models.ForeignKey(
        Consumer,
        on_delete=models.SET_NULL,
        null=True,
    )
    coupon_code = models.CharField(max_length=20, unique=True)
    discount_value_cents = models.PositiveIntegerField()
    generated_at = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return (
            f"{self.coupon_code} saved "
            f"on {self.generated_at.strftime('%Y-%m-%d')}"
        )
