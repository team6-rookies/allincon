from django.urls import path
from .views import *

urlpatterns = [
    path('locations/', LocationListAPIView.as_view(), name='location-list'),
    path('locations/<int:pk>/', LocationRetrieveAPIView.as_view(), name='location-detail'),
    # 특정 Location의 Concert 목록 URL
    path('locations/<int:location_pk>/concerts/', ConcertsByLocationAPIView.as_view(), name='location-concerts'),
    path('sources/', SiteListAPIView.as_view(), name='source-list'),
    path('sources/<int:pk>/', SiteRetrieveAPIView.as_view(), name='source-detail'),
    # 특정 Source의 Concert 목록 URL
    path('sources/<int:source_pk>/concerts/', ConcertsBySiteAPIView.as_view(), name='source-concerts'),
    path('concerts/', ConcertListAPIView.as_view(), name='concert-list'),
    path('concerts/<int:pk>/', ConcertRetrieveAPIView.as_view(), name='concert-detail'),
]