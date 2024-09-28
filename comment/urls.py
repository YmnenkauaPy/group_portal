from django.urls import path
from django.contrib.auth import views as auth_views
from comment import views

urlpatterns = [
    path('comment/update/<int:pk>/', views.edit_comment, name='edit_comment'), 
    path('comment/delete/<int:pk>/', views.delete_comment, name='delete_comment'), 
]