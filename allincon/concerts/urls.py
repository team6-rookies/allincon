# from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'concerts'

urlpatterns = [
    path('', views.index, name='index'),
    path('all_concerts/', views.all_concerts, name='all_concerts'), 
    path('all_locations/', views.all_locations, name='all_locations'), 
    path('all_locations/<int:id>', views.by_location, name='by_location'),
]