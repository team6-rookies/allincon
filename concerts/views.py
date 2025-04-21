from django.shortcuts import render

from django.shortcuts import render, get_object_or_404
from .models import Concert, Location
from django.db.models import Q # 검색용

def index(request):
    """인덱스 페이지 뷰"""
    query = request.GET.get('q')
    if query:
        concerts = Concert.objects.filter(
            Q(title__icontains=query) | Q(location__name__icontains=query)
        ).order_by('start_date')

        context = {
            'query': query,
            'concerts': concerts,
            'is_search_result': True,
        }
        return render(request, 'concerts/all_concerts.html', context)
    return render(request, 'concerts/index.html')

def all_concerts(request):
    """모든 콘서트 목록 페이지 뷰"""
    concert_list = Concert.objects.all()
    context = {'concerts': concert_list, 'is_search_result': False}
    return render(request, 'concerts/all_concerts.html', context)

def list_locations(request):
    """공연장 목록 페이지 뷰"""
    location_list = Location.objects.all()
    context = {'locations': location_list}
    return render(request, 'concerts/list_locations.html', context)

def concerts_by_location(request, location_id):
    """특정 공연장의 콘서트 목록 페이지 뷰"""
    location = get_object_or_404(Location, pk=location_id)
    concert_list = location.concerts.all()
    context = {'location': location, 'concerts': concert_list, 'is_search_result': False}
    return render(request, 'concerts/all_concerts.html', context)