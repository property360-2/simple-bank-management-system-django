from django.urls import path
from . import views

app_name = 'investments'

urlpatterns = [
    path('', views.portfolio_list, name='portfolio_list'),
    path('<int:pk>/', views.portfolio_detail, name='portfolio_detail'),
    path('create/', views.create_portfolio, name='create_portfolio'),
    path('products/', views.products_list, name='products_list'),
    path('<int:portfolio_id>/buy/', views.buy_investment, name='buy_investment'),
    path('holdings/<int:holding_id>/sell/', views.sell_investment, name='sell_investment'),
]
