# urls.py
from django.urls import path
from .views import ConcertUploadView

urlpatterns = [
    path('crawling/', ConcertUploadView.as_view(), name='event-upload'),
]
