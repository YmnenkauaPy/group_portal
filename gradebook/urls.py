from django.urls import path
from django.contrib.auth import views as auth_views
from gradebook import views

urlpatterns = [
    path('grades/', views.grades_list, name='grades_list'),
    path('grades/add/', views.add_grade, name='add_grade'),
    path('grades/edit/<int:pk>/', views.edit_grade, name='edit_grade'),
    path('grades/delete/<int:pk>/', views.delete_grade, name='delete_grade'),
]