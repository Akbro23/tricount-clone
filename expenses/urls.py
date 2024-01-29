from django.urls import path

from . import views


app_name = 'expenses'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('activity/<int:activity_id>/', views.activity, name='activity'),
    path('activity/<int:activity_id>/balance/', views.balance, name='balance'),
    path('activity/<int:activity_id>/create_expense/', views.create_expense, name='create_expense'),
    path('expense/<int:expense_id>/', views.expense, name='expense'),
]