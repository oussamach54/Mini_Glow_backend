# product/urls.py
from django.urls import path
from .views import (
    ProductsList, ProductDetailView, ProductCreateView,
    ProductEditView, ProductDeleteView,
    WishlistListCreateView, WishlistDeleteView, WishlistToggleView,
    ShippingRatesPublicList, ShippingRatesAdminListCreate, ShippingRateAdminDetail,
    BrandsListView,
)

urlpatterns = [
    path("products/", ProductsList.as_view()),
    path("product/<int:pk>/", ProductDetailView.as_view()),
    path("product-create/", ProductCreateView.as_view()),
    path("product-update/<int:pk>/", ProductEditView.as_view()),
    path("product-delete/<int:pk>/", ProductDeleteView.as_view()),

    path("wishlist/", WishlistListCreateView.as_view()),
    path("wishlist/<int:pk>/", WishlistDeleteView.as_view()),
    path("wishlist/toggle/", WishlistToggleView.as_view()),

    path("shipping/", ShippingRatesPublicList.as_view()),
    path("admin/shipping/", ShippingRatesAdminListCreate.as_view()),
    path("admin/shipping/<int:pk>/", ShippingRateAdminDetail.as_view()),

    path("brands/", BrandsListView.as_view()),
]
