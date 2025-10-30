from django.urls import path
from . import views

urlpatterns = [
    # payments
    path("create/", views.CreatePayment.as_view(), name="payments-create"),
    path("order/<int:pk>/status/", views.OrderStatus.as_view(), name="payments-order-status"),
    path("cmi/ok/<int:pk>/", views.CmiOk.as_view(), name="payments-cmi-ok"),
    path("cmi/fail/<int:pk>/", views.CmiFail.as_view(), name="payments-cmi-fail"),
    path("health/", views.Health.as_view(), name="payments-health"),

    # shipping rates
    path("shipping-rates/", views.ShippingRateListCreate.as_view(), name="shipping-rates"),
    # optional admin edit/delete:
    path("admin/shipping-rates/<int:pk>/", views.ShippingRateAdminUpdateDelete.as_view(),
         name="shipping-rate-admin"),
]
