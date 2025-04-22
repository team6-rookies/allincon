from django.shortcuts import render

from django.shortcuts import render, get_object_or_404
from .models import Concert, Location
from django.db.models import Q, Count # 검색용

def index(request):
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
    concert_list = Concert.objects.all()
    context = {'concerts': concert_list, 'is_search_result': False}
    return render(request, 'concerts/all_concerts.html', context)

def concerts_by_location(request, location_id):
    location = get_object_or_404(Location, pk=location_id)
    concert_list = location.concerts.all()
    context = {'location': location, 'concerts': concert_list, 'is_search_result': False}
    return render(request, 'concerts/all_concerts.html', context)

def venue_stats_view(request):
    venue_counts = Location.objects.annotate(
        concert_count = Count('concerts')
        ).filter(
            concert_count__gt=0
        ).values(
            'id', 'name', 'concert_count'
        ).order_by('-concert_count', 'name')
    context = {'venue_stats': venue_counts}
    return render(request, 'concerts/venue_stats.html', context)