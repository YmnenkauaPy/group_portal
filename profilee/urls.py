from django.urls import path
from django.contrib.auth import views as auth_views
from profilee import views

urlpatterns = [
    path('profile_view/', views.profile_view, name='profile_view'),
    path('update_profile/', views.update_profile, name='update_profile'),
]