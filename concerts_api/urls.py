from django.urls import path
from .views import *

urlpatterns = [
    path('concerts/', ConcertListAPIView.as_view(), name='api_concert_list')
]
