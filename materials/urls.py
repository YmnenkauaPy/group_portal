from django.urls import path
from materials import views

urlpatterns = [
    path('materials/<int:page>', views.materials_list, name='materials_list'),
    path('add/material/', views.add_material, name='add_material'),
    path('edit/material/<int:pk>', views.edit_material, name='edit_material'),
    path('delete/material/<int:pk>', views.delete_material, name='delete_material'),
]