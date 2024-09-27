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
    path('calendar/', views.calendar, name='calendar'), 
    path('event/create/<str:day_month_year>', views.create_event, name='create_event'), 
    path('event/delete/<int:pk>', views.delete_event, name='delete_event'), 
    path('event/edit/<int:pk>', views.edit_event, name='edit_event'), 
    path('event/<str:day_month_year>/', views.get_event_data, name='get_event_data'), 
    path('events/<int:year>/<int:month>/', views.events_for_month, name='events_for_month'),
    path('grades/', views.grades_list, name='grades_list'),
    path('grades/add/', views.add_grade, name='add_grade'),
    path('grades/edit/<int:pk>/', views.edit_grade, name='edit_grade'),
    path('grades/delete/<int:pk>/', views.delete_grade, name='delete_grade'),
]
