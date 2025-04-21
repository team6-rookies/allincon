from django.urls import path
from .views import *

urlpatterns = [
    path('concerts/', ConcertCrawlAPIView.as_view(), name='concert-upload'),
]