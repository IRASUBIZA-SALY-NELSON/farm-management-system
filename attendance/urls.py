from django.urls import path
from .views import add_farmer, attendance_list, farmers_list

urlpatterns = [
    path('', attendance_list, name='attendance_list'),
    path('farmers/', farmers_list, name='farmers_list'),
    path('farmers/add/', add_farmer, name='add_farmer'),
]