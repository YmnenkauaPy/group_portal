from django.urls import path 
from event import views

urlpatterns = [
    path('event/create/<str:day_month_year>', views.create_event, name='create_event'), 
    path('event/delete/<int:pk>', views.delete_event, name='delete_event'), 
    path('event/edit/<int:pk>', views.edit_event, name='edit_event'), 
    path('event/<str:day_month_year>/', views.get_event_data, name='get_event_data'), 
    path('events/<int:year>/<int:month>/', views.events_for_month, name='events_for_month'),
    path('calendar/', views.calendar, name='calendar'), 
]