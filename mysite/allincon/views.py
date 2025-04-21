from django.shortcuts import render

from django.http import HttpResponse
from allincon.models import Concert
from allincon_api.serializers import ConcertSerializer

def index(request): #index라는 함수에 요청이 들어오면 Http응답인 hello world 응답하겠다
    #serializer = ConcertSerializer(Concert.objects.all(), many=True)
    #context = {'concerts': serializer.data}
    concerts = Concert.objects.select_related('location').all() # location을 미리 가져와서 쿼리 수를 줄임
    context= {'concerts': concerts}
    return render(request, 'allincon/index.html', context)

# Create your views here.
