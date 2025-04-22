from rest_framework import serializers
from concerts.models import Concert

class ConcertSerializer(serializers.ModelSerializer):
    location = serializers.CharField(source='location.name')
    site = serializers.StringRelatedField()

    class Meta:
        model = Concert
        fields = '__all__' # 모든 필드 JSON에 포함