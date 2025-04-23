from django.shortcuts import render
from .models import Concert, Location, Site
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

# Create your views here.

def index(request):
    return render(request, 'concerts/index.html')

def all_concerts(request):
    concerts = Concert.objects.select_related('location', 'site').all()

    return render(request, 'concerts/all_concerts.html', {'concerts': concerts})

def all_locations(request):
    locations = Location.objects.all()

    return render(request, 'concerts/all_locations.html', {'locations': locations})


def by_location(request, id):
    location = Location.objects.get(pk=id)
    concerts = Concert.objects.filter(location=id)
    
    return render(request, 'concerts/by_location.html', {'location': location.name, 'concerts': concerts})