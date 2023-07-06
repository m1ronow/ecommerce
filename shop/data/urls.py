from django.urls import include, path
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', views.CustomUserViewSet)
router.register(r'user_address', views.UserAddressViewSet)
router.register(r'user_profile', views.UserProfileViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'cart', views.CartViewSet)
router.register(r'cart_items', views.CartItemViewSet)
router.register(r'favorites', views.FavoritesItemViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'order_items', views.OrderItemViewSet)
router.register(r'payments', views.PaymentViewSet)
router.register(r'shipping_methods', views.ShippingMethodViewSet)
router.register(r'payment_methods', views.PaymentMethodViewSet)
router.register(r'promo', views.PromoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('auth_verify/', views.AuthVerifyView.as_view()),
]
