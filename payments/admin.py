from django.contrib import admin
from .models import PaymentOrder, ShippingRate


@admin.register(PaymentOrder)
class PaymentOrderAdmin(admin.ModelAdmin):
    list_display  = ("id", "email", "amount", "currency", "status", "created_at")
    list_filter   = ("status", "currency")
    search_fields = ("id", "email")


@admin.register(ShippingRate)
class ShippingRateAdmin(admin.ModelAdmin):
    list_display  = ("city", "price", "active", "updated_at")
    list_filter   = ("active",)
    search_fields = ("city",)
