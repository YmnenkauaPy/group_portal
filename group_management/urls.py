from django.urls import path
from group_management import views

urlpatterns = [
    path('add_group/', views.add_group, name='add_group'),
    path('search/', views.search_users, name='search_users'),
    path('add/member/<int:group>/', views.add_member, name='add_member'),
    path('delete/member/<int:group>/<int:user>', views.delete_member, name='delete_member'),
    path('update_group/<int:pk>/', views.update_group, name='update_group'),
    path('delete_group/<int:pk>/', views.delete_group, name='delete_group'),
    path('add/moderator/<int:group>/<int:user>', views.add_moderator, name='add_moderator'),
    path('remove/moderator/<int:group>/<int:user>', views.remove_moderator, name='remove_moderator'),
]