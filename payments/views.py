from typing import Any, Dict

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

# If you keep your ShippingRate model/serializer here:
try:
    from .models import ShippingRate
except Exception:  # pragma: no cover
    ShippingRate = None  # type: ignore

try:
    from .serializers import ShippingRateSerializer
except Exception:  # pragma: no cover
    ShippingRateSerializer = None  # type: ignore


# ---------- Helpers to build frontend redirect URLs ----------

def _frontend_success_url(request, order_id: int) -> str:
    base = getattr(settings, "CMI_SUCCESS_URL", None)
    if base:
        sep = "&" if "?" in base else "?"
        return f"{base}{sep}order={order_id}"

    frontend = getattr(settings, "FRONTEND_URL", "")
    if frontend:
        return f"{frontend.rstrip('/')}/payment-status?order={order_id}"

    return f"/payment-status?order={order_id}"


def _frontend_fail_url(request, order_id: int) -> str:
    base = getattr(settings, "CMI_FAIL_URL", None)
    if base:
        sep = "&" if "?" in base else "?"
        return f"{base}{sep}order={order_id}"

    frontend = getattr(settings, "FRONTEND_URL", "")
    if frontend:
        return f"{frontend.rstrip('/')}/payment-status?order={order_id}&status=failed"

    return f"/payment-status?order={order_id}&status=failed"


# ---------- Payments (minimal versions so routes exist) ----------

class CreatePayment(APIView):
    """
    Minimal placeholder that pretends a payment session was created.
    Replace with your real gateway integration as needed.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        payload: Dict[str, Any] = request.data or {}
        # Here you would create an Order + PaymentSession and return its URL.
        # We return a stub payload so your frontend can continue.
        fake_order_id = payload.get("order_id") or 1
        return Response(
            {
                "ok": True,
                "order_id": fake_order_id,
                "payment_url": _frontend_success_url(request, fake_order_id),
            },
            status=status.HTTP_201_CREATED,
        )


class OrderStatus(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk: int, *args, **kwargs):
        # Replace with real lookup (e.g., Order.objects.get(pk=pk))
        # We return a stub “paid:false” status for now.
        return Response({"order_id": pk, "paid": False, "status": "pending"})


class CmiOk(APIView):
    authentication_classes = []  # callbacks are usually unauthenticated
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk: int, *args, **kwargs):
        return HttpResponseRedirect(_frontend_success_url(request, pk))


class CmiFail(APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk: int, *args, **kwargs):
        return HttpResponseRedirect(_frontend_fail_url(request, pk))


class Health(APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        return Response({"ok": True})


class CheckToken(APIView):
    """
    Used by the frontend to validate the current JWT.
    Returns 200 when the token is valid, 401 otherwise.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({"ok": True, "user": getattr(request.user, "username", None)})


# ---------- Shipping Rates (requires model & serializer) ----------

class ShippingRateListCreate(generics.ListCreateAPIView):
    """
    GET  /api/payments/shipping-rates/   -> list (public)
    POST /api/payments/shipping-rates/   -> create (admin)
    """
    queryset = ShippingRate.objects.all() if ShippingRate else []  # type: ignore
    serializer_class = ShippingRateSerializer
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        if self.request.method.lower() == "post":
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class ShippingRateAdminUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShippingRate.objects.all() if ShippingRate else []  # type: ignore
    serializer_class = ShippingRateSerializer
    permission_classes = [permissions.IsAdminUser]
