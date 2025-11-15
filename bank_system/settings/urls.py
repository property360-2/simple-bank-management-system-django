from django.urls import path
from . import views

app_name = 'settings'

urlpatterns = [
    path('', views.settings_dashboard, name='dashboard'),
    path('profile/', views.profile_edit, name='profile_edit'),
    path('password/', views.change_password, name='change_password'),
    path('security/', views.security_settings, name='security'),
    path('accounts/', views.account_summary, name='account_summary'),
]
