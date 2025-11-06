from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from my_project.health import health

# ✅ SimpleJWT views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Your existing apps
    path('api/', include('product.urls')),
    path('payments/', include('payments.urls')),
    path('account/', include('account.urls')),
    path('api/newsletter/', include('newsletter.urls')),
    path('health/', health),

    # ✅ Add the standard SimpleJWT endpoints at /api/token/*
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

# Static & media (dev and simple deployments)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
