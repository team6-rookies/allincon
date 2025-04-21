from django.urls import path
from . import views

app_name = 'concerts'

urlpatterns = [
    path('', views.index, name='index'),
    path('all/', views.all_concerts, name='all_concerts'),
    path('locations/', views.list_locations, name='list_locations'),
    path('location/<int:location_id>/', views.concerts_by_location, name='concerts_by_location'),
]