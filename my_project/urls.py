from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from my_project.health import health
from account.views import MyTokenObtainPairView   # <— add this import

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT token pair (the endpoint your frontend calls)
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),

    # App routers
    path('api/', include('product.urls')),
    path('payments/', include('payments.urls')),
    path('account/', include('account.urls')),  # still keep /account/login/ etc.
    path('api/newsletter/', include('newsletter.urls')),

    # Health
    path('health/', health),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
