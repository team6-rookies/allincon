from rest_framework import serializers
from allincon.models import *

class ConcertSerializer(serializers.ModelSerializer):
    # location = serializers.SlugRelatedField(
    #     slug_field='name',
    #     queryset=Location.objects.all()
    # )
    class Meta:
        model = Concert
        fields = ['id', 'title', 'location', 'start_date', 'end_date']