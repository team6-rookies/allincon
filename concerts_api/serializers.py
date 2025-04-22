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

class ConcertWriteSerializer(serializers.ModelSerializer):
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

class ConcertListSerializer(serializers.ModelSerializer):
    location = serializers.StringRelatedField(read_only=True)
    source = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Concert
        fields = [
            'id', 'title', 'location', 'start_date', 'end_date', 'source',
        ]

class VenueConcertCountSerializer(serializers.Serializer):
    name = serializers.CharField(help_text="공연장 이름")
    concert_count = serializers.IntegerField(help_text="해당 공연장의 콘서트 수")