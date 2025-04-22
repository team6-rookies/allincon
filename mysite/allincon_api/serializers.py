from rest_framework import serializers
from allincon.models import *



class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = ['id','name']

        
class ConcertSerializer(serializers.ModelSerializer):
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
        # location이 문자열로 들어오는 경우 처리 현재는 이 부분으로 분기된다.
        else:
            location_obj, _ = Location.objects.get_or_create(name=location) # _ 는 반환값의 두 번째 요소를 사용하지 않겠다는 의미.
        
        # site가 숫자(id)로 들어오는 경우 처리
        if isinstance(site, str) and site.isdigit():
            site_obj = Site.objects.get(pk=site)
        # site가 문자열로 들어오는 경우 처리 현재는 이 부분으로 분기된다.
        else:
            site_obj, _ = Site.objects.get_or_create(name=site)

        concert = Concert.objects.create(location=location_obj, site=site_obj, **validated_data)
        return concert
    class Meta:
        model = Concert
        fields = ['title', 'location', 'start_date', 'end_date','site']

class LocationSerializer(serializers.ModelSerializer):
    concert_count = serializers.IntegerField(read_only=True) 
    closest_concert = ConcertSerializer(read_only=True)  # read_only로 설정
    # 장소별 콘서트의 수를 한눈에 출력하고 싶은데 html에 정보를 넘길때 이미 각 장소에서 열리는 콘서트의 개수라는 가상 필드(읽기전용 출력할때만 쓰기 위함)concert_count 필드 추가
    class Meta:
        model = Location
        fields = ['id','name','address','max_people','concert_count','closest_concert']


#views.py에서 LocationListView를 통해서 html에 꼭 serializer해서 넘기고 싶은데 조금더 수정필요할듯 
#좀 불필요한 부분이 있음 LcationSerializer만을 사용해서 직렬화도 될꺼 같은데 조금만 더 생각
class LocationDataSerializer(serializers.Serializer):
    location = LocationSerializer()
    concert_count = serializers.IntegerField()
    closest_concert = ConcertSerializer()
