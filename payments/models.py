from django.db import models
from django.utils import timezone


class PaymentOrder(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PAID    = "paid",    "Paid"
        FAILED  = "failed",  "Failed"
        CANCELED= "canceled","Canceled"

    amount      = models.DecimalField(max_digits=10, decimal_places=2)
    currency    = models.CharField(max_length=8, default="MAD")
    email       = models.EmailField(blank=True, null=True)
    status      = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING)
    payload     = models.JSONField(default=dict, blank=True)
    customer_ip = models.GenericIPAddressField(null=True, blank=True)

    created_at  = models.DateTimeField(default=timezone.now)
    updated_at  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.pk} - {self.amount} {self.currency} - {self.status}"


class ShippingRate(models.Model):
    city   = models.CharField(max_length=120, unique=True)
    price  = models.DecimalField(max_digits=8, decimal_places=2)
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["city"]

    def __str__(self):
        return f"{self.city} - {self.price} MAD"
