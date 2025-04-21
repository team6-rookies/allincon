from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('all_in_one_app/',views.wholeConcert, name='all-in-one-app'), 
    path('location_agg_app/',views.locationAgg, name='location-agg-app'),
    path('location_group_app/<int:location_id>/',views.locationDetail, name='location-detail'),
]