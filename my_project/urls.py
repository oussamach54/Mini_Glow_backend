from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from my_project.health import health

from rest_framework_simplejwt.views import TokenRefreshView
from account.views import MyTokenObtainPairView


urlpatterns = [
    path('admin/', admin.site.urls),
     # JWT
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # ✅ Everything behind /api/
    path('api/', include('product.urls')),           # products, wishlist, brands, shipping (product app)
    path('api/payments/', include('payments.urls')), # payments + shipping-rates (payments app)
    path('api/account/', include('account.urls')),   # account endpoints
    path('health/', health),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 


 