from django.urls import path
from django.contrib.auth import views as auth_views
from forum import views

urlpatterns = [
    path('thread/new/', views.thread_create, name='thread_create'),  
    path('edit/<int:pk>/', views.thread_update, name='edit_thread'), 
    path('detail/<int:pk>/', views.ThreadDetailView.as_view(template_name="forum/thread_detail.html"), name='thread_detail'), 
    path('threads/<int:page>', views.thread_list, name='thread_list'),  
]