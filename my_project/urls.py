# my_project/urls.py
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve as static_serve

from my_project.health import health
from account.views import MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # APIs
    path('api/', include('product.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/account/', include('account.urls')),
    path('api/newsletter/', include('newsletter.urls')),

    path('health/', health),

    # ------------ MEDIA (uploads) ALWAYS ON ------------
    # This makes /images/... map to MEDIA_ROOT even when DEBUG=False (Coolify)
    re_path(r'^images/(?P<path>.*)$',
            static_serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# (debug helper for static won't run in prod; media already handled above)

