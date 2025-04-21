# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('concerts/', ConcertListView.as_view(), name='concert-list'), ## get으로 들어오면전체 콘서트 리스트 조회 #post로 들어오면 콘서트 정보 추가
    path('locations/', LocationListView.as_view(), name='location-list'),
    path('locations/<int:location_id>/', ConcertByLocationView.as_view(), name='concert-by-location'),
]
