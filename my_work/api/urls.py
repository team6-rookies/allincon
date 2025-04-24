from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', views.ConcertSearchView.as_view(), name='concert-search'),
    path('concerts/', views.ConcertListView.as_view(), name='concert-list'),
    path('locations/', views.LocationListView.as_view(), name='location-list'),
    path('locations/<int:location_id>/concerts/', views.ConcertsByLocationView.as_view(), name='concerts-by-location'),
]
