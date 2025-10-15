from django.urls import path
from . import views

urlpatterns = [
    path('', views.transaction_list, name='transaction_list'),
    path('deposit/<int:account_pk>/', views.deposit, name='deposit'),
    path('withdraw/<int:account_pk>/', views.withdraw, name='withdraw'),
    path('transfer/<int:account_pk>/', views.transfer, name='transfer'),
]