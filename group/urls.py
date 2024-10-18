from django.urls import path
from group import views

urlpatterns = [
    path('', views.group_list, name='group_list'),
    path('group/<int:pk>/', views.group_detail, name='group_detail'), 
]