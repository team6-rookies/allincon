# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('concerts/', ConcertListView.as_view(), name='concert-list'), # get으로 들어오면전체 콘서트 리스트 조회 #post로 들어오면 콘서트 정보 추가
    path('locations/', LocationListView.as_view(), name='location-list'),#전체 location 리스트 조회
    path('locations/<int:location_id>/', ConcertByLocationView.as_view(), name='concert-by-location'),# location_id에 해당하는 콘서트 리스트 조회
    path('concerts/month', ConcertMonthView.as_view(), name='concert-month'),# 월별 콘서트 수 및 제목 조회
]
