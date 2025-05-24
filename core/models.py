from django.db import models
from marketplace.models import Company
from django.conf import settings
from marketplace.models import Coupon

class GeneralAdministrator(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True
    )
    phone = models.CharField(max_length=14)  # telefone do administrador

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class CouponReceipt(models.Model):
    coupon = models.OneToOneField(Coupon, on_delete=models.PROTECT)
    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True
    )
    file = models.FileField(upload_to='receipts/coupons')
    date = models.DateTimeField()

    def __str__(self):
        return f"Coupon Receipt {self.coupon.code}"


class PaymentReceipt(models.Model):
    coupon_receipt = models.ForeignKey(
        CouponReceipt,
        on_delete=models.PROTECT
    )
    administrator = models.ForeignKey(
        GeneralAdministrator,
        on_delete=models.SET_NULL,
        null=True
    )
    amount = models.PositiveIntegerField(
        help_text="Stored in cents. For example: 199 = R$1.99"
    )
    file = models.FileField(upload_to='receipts/payment')
    paid_at = models.DateTimeField()

    def __str__(self):
        value_amount = self.amount/100
        return (
            f"Payment Receipt {self.pk} with "
            f"value amount R${value_amount:2f} "
            f"on {self.paid_at.strftime('%Y-%m-%d')}"
        )


class CompanyBankAccount(models.Model):
    class BankChoices(models.TextChoices):
        BANCO_DO_BRASIL = "001", "Banco do Brasil"
    
    class AccountTypeChoices(models.TextChoices):
        CURRENT = "current", "Current"
        SAVING = "saving", "Saving"
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    bank = models.CharField(max_length=255, choices=BankChoices.choices)
    agency = models.CharField(max_length=10)
    account = models.CharField(max_length=20)
    account_type = models.CharField(
        max_length=20,
        choices=AccountTypeChoices.choices
    )
    pix_key = models.CharField(max_length=255, null=True, blank=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return (
            f"{self.company.name} - {self.account} "
            f"(Agency: {self.agency}, "
            f"Bank: {self.get_bank_display()})"
        )
