# account/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import StripeModel, BillingAddress, OrderModel


class UserSerializer(serializers.ModelSerializer):
    admin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "admin"]

    def get_admin(self, obj):
        return obj.is_staff


class UserRegisterTokenSerializer(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "admin", "token"]

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)


class CardsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = StripeModel
        fields = "__all__"


class BillingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingAddress
        fields = "__all__"


class AllOrdersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderModel
        fields = "__all__"


# ----- NEW: creation serializer for COD orders -----
class OrderCODCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderModel
        fields = [
            "items",
            "total_price",
            "customer_name",
            "phone",
            "address",
            "city",
            "notes",
        ]

    def validate(self, attrs):
        if not attrs.get("phone"):
            raise serializers.ValidationError("Le téléphone est requis.")
        if not attrs.get("address"):
            raise serializers.ValidationError("L’adresse est requise.")
        if attrs.get("total_price") in (None, ""):
            raise serializers.ValidationError("Le total est requis.")
        return attrs
