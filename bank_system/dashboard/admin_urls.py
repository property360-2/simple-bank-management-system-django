from django.urls import path, include
from . import admin_views
from investments import admin_views as investment_admin_views
from savings import admin_views as savings_admin_views

app_name = 'admin_panel'

# Admin dashboard and fraud detection
dashboard_patterns = [
    path('', admin_views.admin_dashboard, name='dashboard'),
    path('fraud-detection/', admin_views.fraud_detection_list, name='fraud_detection_list'),
    path('fraud-detection/<int:pk>/', admin_views.fraud_detection_detail, name='fraud_detection_detail'),
]

# Investment product management
investment_patterns = [
    path('investment-products/', investment_admin_views.investment_products_list, name='investment_products_list'),
    path('investment-products/create/', investment_admin_views.investment_product_create, name='investment_product_create'),
    path('investment-products/<int:pk>/edit/', investment_admin_views.investment_product_edit, name='investment_product_edit'),
    path('investment-products/<int:pk>/delete/', investment_admin_views.investment_product_delete, name='investment_product_delete'),
    path('investment-platforms/', investment_admin_views.investment_platforms_list, name='investment_platforms_list'),
    path('investment-platforms/create/', investment_admin_views.investment_platform_create, name='investment_platform_create'),
    path('investment-platforms/<int:pk>/edit/', investment_admin_views.investment_platform_edit, name='investment_platform_edit'),
    path('investment-platforms/<int:pk>/delete/', investment_admin_views.investment_platform_delete, name='investment_platform_delete'),
]

# Savings product management
savings_patterns = [
    path('savings-products/', savings_admin_views.savings_products_list, name='savings_products_list'),
    path('savings-products/create/', savings_admin_views.savings_product_create, name='savings_product_create'),
    path('savings-products/<int:pk>/edit/', savings_admin_views.savings_product_edit, name='savings_product_edit'),
    path('savings-products/<int:pk>/delete/', savings_admin_views.savings_product_delete, name='savings_product_delete'),
]

urlpatterns = dashboard_patterns + investment_patterns + savings_patterns
