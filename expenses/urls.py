from django.urls import path

from . import views


app_name = 'expenses'
urlpatterns = [   
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('create_activity/', views.create_activity, name='create_activity'),
    path('activity/<int:activity_id>/', views.activity, name='activity'),
    path('activity/<int:activity_id>/balance/', views.balance, name='balance'),
    path('activity/<int:activity_id>/add_participant/', views.add_participant, name='add_participant'),
    path('activity/<int:activity_id>/remove_participant/<int:participant_id>', views.remove_participant, name='remove_participant'),
    path('activity/<int:activity_id>/create_expense/', views.create_expense, name='create_expense'),     
    path('expense/<int:expense_id>/', views.expense, name='expense'),  
    path('expense/<int:expense_id>/delete/', views.delete_expense, name='delete_expense'),
]