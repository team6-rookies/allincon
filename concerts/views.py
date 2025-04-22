from django.shortcuts import render, get_object_or_404
from .models import Concert, Location

# Create your views here.

def index(request):
    return render(request, 'concerts/index.html')

def concert_list(request):
    query = request.GET.get('query') # 검색어
    search_type = request.GET.get('search_type') # 검색 타입
    concerts = Concert.objects.all().order_by('start_date')

    if query and search_type:
        if search_type == 'title':
            concerts = concerts.filter(title__icontains=query)
        elif search_type == 'location':
            concerts = concerts.filter(location__name__icontains=query)
        elif search_type == 'start_date':
            concerts = concerts.filter(start_date__icontains=query)

    return render(request, 'concerts/concert_list.html', {'concerts':concerts})

def location_list(request):
    locations = Location.objects.filter(concerts__isnull=False).distinct()
    return render(request, 'concerts/location_list.html', {'locations':locations})

def concerts_by_location(request, location):
    # location은 문자열 -> Location 모델에서 name으로 찾기
    location_obj = get_object_or_404(Location, name=location)
    
    concerts = Concert.objects.filter(location=location_obj).order_by('start_date')
    return render(request, 'concerts/concerts_by_location.html', {'concerts':concerts, 'clicked_location':location})