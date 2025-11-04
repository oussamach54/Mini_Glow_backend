# account/urls.py
from django.urls import path
from .views import (
    UserRegisterView,
    MyTokenObtainPairView,   # only used by project-level /api/token/, not mounted here
    GoogleLoginView,
    CardsListView,
    UserAccountDetailsView,
    UserAccountUpdateView,
    UserAccountDeleteView,
    UserAddressesListView,
    CreateUserAddressView,
    UserAddressDetailsView,
    UpdateUserAddressView,
    DeleteUserAddressView,
    OrdersListView,
    ChangeOrderStatus,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    CreateCODOrderView,
)

urlpatterns = [
    # Registration & social
    path('register/', UserRegisterView.as_view(), name='register'),
    path('google-login/', GoogleLoginView.as_view(), name='google_login'),

    # Cards (me)
    path('cards/', CardsListView.as_view(), name='cards'),

    # Users
    path('users/<int:pk>/', UserAccountDetailsView.as_view(), name='user_details'),
    path('users/<int:pk>/update/', UserAccountUpdateView.as_view(), name='user_update'),
    path('users/<int:pk>/delete/', UserAccountDeleteView.as_view(), name='user_delete'),

    # Aliases used by old frontend (kept for compatibility)
    path('user/<int:pk>/', UserAccountDetailsView.as_view(), name='user_details_alias'),
    path('user_update/<int:pk>/', UserAccountUpdateView.as_view(), name='user_update_alias'),
    path('user_delete/<int:pk>/', UserAccountDeleteView.as_view(), name='user_delete_alias'),

    # Addresses (me)
    path('addresses/', UserAddressesListView.as_view(), name='addresses_list'),
    path('addresses/create/', CreateUserAddressView.as_view(), name='address_create'),
    path('addresses/<int:pk>/', UserAddressDetailsView.as_view(), name='address_details'),
    path('addresses/<int:pk>/update/', UpdateUserAddressView.as_view(), name='address_update'),
    path('addresses/<int:pk>/delete/', DeleteUserAddressView.as_view(), name='address_delete'),

    # Old address aliases the frontend calls
    path('all-address-details/', UserAddressesListView.as_view(), name='addr_list_alias'),
    path('create-address/', CreateUserAddressView.as_view(), name='addr_create_alias'),
    path('address-details/<int:pk>/', UserAddressDetailsView.as_view(), name='addr_detail_alias'),
    path('update-address/<int:pk>/', UpdateUserAddressView.as_view(), name='addr_update_alias'),
    path('delete-address/<int:pk>/', DeleteUserAddressView.as_view(), name='addr_delete_alias'),

    # Orders
    path('orders/', OrdersListView.as_view(), name='orders_list'),
    path('orders/<int:pk>/status/', ChangeOrderStatus.as_view(), name='order_change_status'),
    path('orders/cod/', CreateCODOrderView.as_view(), name='create_cod_order'),

    # Old orders alias
    path('all-orders-list/', OrdersListView.as_view(), name='orders_list_alias'),

    # Password reset
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # Old aliases the frontend uses
    path('account/password-reset/', PasswordResetRequestView.as_view(), name='password_reset_alias'),
    path('account/password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm_alias'),
]
