from django.urls import path
from . import views

urlpatterns = [
    # The name is 'manager_dashboard'
    path('dashboard/', views.dashboard, name='manager_dashboard'),

    path('add-product/', views.add_product, name='add_product'),
    path('delete-product/<int:pk>/', views.delete_product, name='delete_product'),
    path('orders/', views.view_orders, name='view_orders'),
    path('orders/<int:order_id>/', views.order_detail, name='admin_order_detail'),
    path('orders/<int:order_id>/update-status/', views.order_update_status, name='admin_order_update_status'),
    path('users/', views.view_users, name='view_users'),
    path('reports/', views.sales_report, name='sales_report'),
]