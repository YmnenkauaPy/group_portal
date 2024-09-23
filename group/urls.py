from django.urls import path
from django.contrib.auth import views as auth_views
from group import views

urlpatterns = [
    path('', views.group_list, name='group_list'),
    path('<int:pk>/', views.group_detail, name='group_detail'), 
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('profile_view/', views.profile_view, name='profile_view'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('thread/new/', views.thread_create, name='thread_create'),  
    path('edit/<int:pk>/', views.thread_update, name='edit_thread'), 
    path('detail/<int:pk>/', views.ThreadDetailView.as_view(template_name="forum/thread_detail.html"), name='thread_detail'), 
    path('threads/', views.thread_list, name='thread_list'),  
    path('comment/update/<int:pk>/', views.edit_comment, name='edit_comment'), 
    path('comment/delete/<int:pk>/', views.delete_comment, name='delete_comment'), 
    path('comment/like/<int:pk>/', views.CommentLikeToggle.as_view(), name='like_comment'), 
]
