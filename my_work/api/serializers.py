from rest_framework import serializers
from concerts.models import *

class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = ['site_id', 'site_name']

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['location_id', 'location_name']


class ConcertSerializer(serializers.ModelSerializer):
    location_name = serializers.CharField(source='location.location_name')
    site_name = serializers.CharField(source='site.site_name')

    class Meta:
        model = Concert
        fields = ['concert_id', 'title', 'start_date', 'end_date', 'location_name', 'site_name']