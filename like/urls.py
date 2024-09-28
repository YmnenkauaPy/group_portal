from django.urls import path
from django.contrib.auth import views as auth_views
from like import views

urlpatterns = [
   path('comment/like/<int:pk>/', views.CommentLikeToggle.as_view(), name='like_comment'), 
]