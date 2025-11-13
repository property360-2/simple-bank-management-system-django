from django.urls import path
from . import views

app_name = 'savings'

urlpatterns = [
    path('', views.savings_list, name='savings_list'),
    path('<int:pk>/', views.savings_detail, name='savings_detail'),
    path('create/', views.create_savings_account, name='create_savings_account'),
    path('<int:savings_account_id>/goals/create/', views.create_goal, name='create_goal'),
    path('goals/', views.goals_list, name='goals_list'),
]
