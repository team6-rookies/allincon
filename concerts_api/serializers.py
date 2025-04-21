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
    location = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(),
        required=False,
        allow_null=True
    )
    source = serializers.PrimaryKeyRelatedField(
        queryset=Site.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Concert
        fields = [
            'id', 'title', 'location', 'start_date', 'end_date', 'source',
            ]