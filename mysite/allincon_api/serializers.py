from rest_framework import serializers
from allincon.models import *


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id','name','address','max_people']

class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = ['id','name']

        
class ConcertSerializer(serializers.ModelSerializer):
    # site = SiteSerializer()
    # location = LocationSerializer()
    # location = serializers.SlugRelatedField(
    #     slug_field='name',
    #     queryset=Location.objects.all()
    # )
    # site = serializers.SlugRelatedField(
    #     slug_field='name',
    #     queryset=Site.objects.all()
    # )
    # 외래키는 기본적으로 해당 모델의 pk값을 기본으로 하는데 SlugRelatedField는 
    # 외래키의 다른 필드를 사용하고 싶을때 slug_field='name'으로 설정하면 
    #해당 모델의 name 필드로 Concert 모델을 직렬화시킨다. 
    #자동적으로 Location.objects.get(name="올림픽공원")을 실행시켜서 해당되는 장소 이름을
    #concert에 넣어서 직렬화하는건데 만약 해당 장소이름이 db에 없으면 오류가 발생해
    #그래서 get_or_create를 사용해서 db에 없으면 새로 생성하는 방식으로 처리하고 싶어
    location = serializers.CharField()
    site = serializers.CharField()
    def create(self, validated_data):
        location = validated_data.pop('location')
        site = validated_data.pop('site')

        # location이 숫자(id)로 들어오는 경우 처리
        if isinstance(location, str) and location.isdigit():
            location_obj = Location.objects.get(pk=location)
        else:
            location_obj, _ = Location.objects.get_or_create(name=location)

        if isinstance(site, str) and site.isdigit():
            site_obj = Site.objects.get(pk=site)
        else:
            site_obj, _ = Site.objects.get_or_create(name=site)

        concert = Concert.objects.create(location=location_obj, site=site_obj, **validated_data)
        return concert
    

    

    # def create(self, validated_data):
    #     location = validated_data.pop('location') ## location은 LocationSerializer로 직렬화된 값이기 때문에
    #     site = validated_data.pop('site')## site는 SiteSerializer로 직렬화된 값이기 때문에
    #     location_obj, _ = Location.objects.get_or_create(name=location)
    #     site_obj, _ = Site.objects.get_or_create(name=site)        

    #     concert = Concert.objects.create(location=location_obj, site=site_obj, **validated_data)
    #     return concert

    class Meta:
        model = Concert
        fields = ['title', 'location', 'start_date', 'end_date','site']
