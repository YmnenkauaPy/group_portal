from django.urls import path
from group_management import views

urlpatterns = [
    path('add_group/', views.add_group, name='add_group'),
    path('update_group/<int:pk>/', views.update_group, name='update_group'),
    path('delete_group/<int:pk>/', views.delete_group, name='delete_group'),
]