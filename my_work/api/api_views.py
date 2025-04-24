from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from concerts.models import Concert, Location
from .serializers import ConcertSerializer, LocationSerializer

# 콘서트 목록
class ConcertListAPIView(generics.ListAPIView):
    queryset = Concert.objects.all()
    serializer_class = ConcertSerializer

# 장소 목록
class LocationListAPIView(generics.ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

# 장소 별 콘서트
class ConcertsByLocationAPIView(generics.ListAPIView):
    serializer_class = ConcertSerializer

    def get_queryset(self):
        location_id = self.kwargs['location_id']
        return Concert.objects.filter(location__location_id=location_id)

# 검색 기능
class ConcertSearchAPIView(APIView):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '')
        concerts = Concert.objects.all()

        if query:
            concerts = concerts.filter(
                Q(title__icontains=query) |
                Q(start_date__icontains=query) |
                Q(end_date__icontains=query) |
                Q(location__location_name__icontains=query) |
                Q(site__site_name__icontains=query)
            )

        serializer = ConcertSerializer(concerts, many=True)
        return Response(serializer.data)
