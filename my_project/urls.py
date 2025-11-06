# my_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from my_project.health import health
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

urlpatterns = [
    path("admin/", admin.site.urls),

    # products under /api/
    path("api/", include("product.urls")),

    # account exposed under both (so frontend deploys with/without /api work)
    path("account/", include("account.urls")),
    path("api/account/", include("account.urls")),

    # payments under both as well
    path("payments/", include("payments.urls")),
    path("api/payments/", include("payments.urls")),

    # optional newsletter
    path("api/newsletter/", include("newsletter.urls")),

    # health
    path("health/", health),

    # keep SimpleJWT refresh/verify if you need them
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
