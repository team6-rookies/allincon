from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.concert_list, name='concert_list'),
    path('locations/', views.location_list, name='location_list'), # 장소별 링크
    path('locations/<str:location>', views.concerts_by_location, name='concerts_by_location'), # 장소별 콘서트 목록
]