from django.urls import path
from .views import add_farmer

urlpatterns = [
    path('farmers/add/', add_farmer, name='add_farmer'),
]