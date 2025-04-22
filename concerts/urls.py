from django.urls import path
from . import views

app_name = 'concerts'

urlpatterns = [
    path('', views.index, name='index'),
    path('all/', views.all_concerts, name='all_concerts'),
    path('locations/', views.venue_stats_view, name='venue_stats'),
    path('location/<int:location_id>/', views.concerts_by_location, name='concerts_by_location'),
]