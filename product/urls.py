from django.urls import path
from product import views

urlpatterns = [
    # Produits
    path("products/", views.ProductsList.as_view(), name="products-list"),
    path("product/<int:pk>/", views.ProductDetailView.as_view(), name="product-details"),
    path("product-create/", views.ProductCreateView.as_view(), name="product-create"),
    path("product-update/<int:pk>/", views.ProductEditView.as_view(), name="product-update"),
    path("product-delete/<int:pk>/", views.ProductDeleteView.as_view(), name="product-delete"),

    # Wishlist
    path("wishlist/", views.WishlistListCreateView.as_view(), name="wishlist-list-create"),
    path("wishlist/toggle/", views.WishlistToggleView.as_view(), name="wishlist-toggle"),
    path("wishlist/<int:pk>/", views.WishlistDeleteView.as_view(), name="wishlist-delete"),

    # Tarifs de livraison
    path("shipping-rates/", views.ShippingRatesPublicList.as_view(), name="shipping-rates-public"),
    path("admin/shipping-rates/", views.ShippingRatesAdminListCreate.as_view(), name="shipping-rates-admin"),
    path("admin/shipping-rates/<int:pk>/", views.ShippingRateAdminDetail.as_view(), name="shipping-rate-admin-detail"),

    # Marques
    path("brands/", views.BrandsListView.as_view(), name="brands-list"),
]
