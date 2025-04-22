from django.urls import path
from .views import *

urlpatterns = [
    path('filter/', ConcertListAPIView.as_view(), name='concert_filter')
]
