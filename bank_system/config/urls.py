from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as user_views
from users.views import CustomLoginView
from dashboard import views as dashboard_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication
    path('register/', user_views.register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Dashboard
    path('', dashboard_views.dashboard, name='dashboard'),

    # Admin Panel
    path('admin-panel/', include('dashboard.admin_urls')),

    # Apps
    path('accounts/', include('accounts.urls')),
    path('transactions/', include('transactions.urls')),
    path('savings/', include('savings.urls')),
    path('investments/', include('investments.urls')),
    path('settings/', include('settings.urls')),
]