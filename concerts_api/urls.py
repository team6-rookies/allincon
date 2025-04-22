from django.urls import path
from .views import *

urlpatterns = [
    path('concerts/', ConcertListView.as_view(), name='concert-list'),
    path('concerts/upload/', ConcertCrawlAPIView.as_view(), name='concert-upload'),
    path('stats/venue-count/', VenueConcertCountView.as_view(), name='venue-stats'),
]
