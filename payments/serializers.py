from rest_framework import serializers
from .models import ShippingRate, PaymentOrder


class ShippingRateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ShippingRate
        fields = "__all__"


class PaymentOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model  = PaymentOrder
        fields = "__all__"
