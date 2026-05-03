from django.urls import path
from . import views

urlpatterns = [
    # Basic Pages
    path('', views.home, name='home'),
    path('collections/', views.collections, name='collections'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),  # <--- Added About

    # Product & Shop
    path('products/', views.products, name='products'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),

    # Cart System
    path('cart/', views.view_cart, name='cart'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<int:item_id>/<str:action>/', views.update_cart, name='update_cart'),
    
    # User System
    path('profile/', views.profile, name='profile'),
    path('register/', views.register_view, name='register'),
    path('checkout/', views.place_order, name='place_order'),

    # Auth System
    path('login/', views.unified_login, name='login'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('logout/', views.signout_view, name='logout'), # <--- Added Logout

    path('signout/', views.signout_view, name='signout'),
]