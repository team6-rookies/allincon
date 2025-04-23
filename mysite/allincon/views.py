from django.shortcuts import render

from django.http import HttpResponse
from allincon.models import *
from allincon_api.serializers import ConcertSerializer


def index(request): #index라는 함수에 요청이 들어오면 Http응답인 hello world 응답하겠다
    #serializer = ConcertSerializer(Concert.objects.all(), many=True)
    #context = {'concerts': serializer.data}
    #concerts = Concert.objects.select_related('location').all() # location을 미리 가져와서 쿼리 수를 줄임
    #context= {'concerts': concerts}
    return render(request, 'allincon/index.html')

def locationAgg(request): #location에 저장된 모든 location을 가져와서 location_agg_app.html에 전달
    locations= Location.objects.all() # location을 중복없이 가져옴
    context= {'locations': locations}
    return render(request, 'allincon/location_agg_app.html', context)

def locationDetail(request, location_id): #location_id에 해당하는 location의 id를 가져와서 location_group_app.html에 전달
    location = Location.objects.get(id=location_id) # location_id에 해당하는 location을 가져옴
    concerts = Concert.objects.filter(location=location) # location에 해당하는 concert를 가져옴
    context = {'location': location, 'concerts': concerts}
    return render(request, 'allincon/location_group_app.html', context)
    
    

def wholeConcert(request): #index라는 함수에 요청이 들어오면 Http응답인 hello world 응답하겠다
    #serializer = ConcertSerializer(Concert.objects.all(), many=True)
    #context = {'concerts': serializer.data}
    concerts = Concert.objects.select_related('location').all() # location을 미리 가져와서 쿼리 수를 줄임
    context= {'concerts': concerts}
    return render(request, 'allincon/all_in_one_app.html', context)
# Create your views here.
