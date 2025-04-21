from rest_framework import serializers
from concerts.models import Location, Concert, Site

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name']

class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = ['id', 'name']

class ConcertSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    source = SiteSerializer(read_only=True)

    class Meta:
        model = Concert
        fields = ['id', 'title', 'location', 'start_date', 'end_date', 'source']