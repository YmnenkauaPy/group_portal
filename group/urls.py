from django.urls import path
from django.contrib.auth import views as auth_views
from group import views

urlpatterns = [
    path('', views.group_list, name='group_list'),
    path('<int:pk>/', views.group_detail, name='group_detail'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('register/', views.register, name='register'),
]
