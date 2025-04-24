from django.urls import path
from . import api_views

urlpatterns = [
    path('concerts/', api_views.ConcertListAPIView.as_view(), name='api-concert-list'),
    path('locations/', api_views.LocationListAPIView.as_view(), name='api-location-list'),
    path('locations/<int:location_id>/concerts/', api_views.ConcertsByLocationAPIView.as_view(), name='api-concerts-by-location'),
]
