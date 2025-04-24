from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.exceptions import NotFound
from concerts.models import Concert, Location, Site
from .serializers import ConcertSerializer, LocationSerializer
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView

# 콘서트 목록
class ConcertListView(ListView):
    model = Concert
    template_name = 'api/concert_list.html'
    context_object_name = 'concerts'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q', None)

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | 
                Q(start_date__icontains=query) |
                Q(end_date__icontains=query) |
                Q(location__location_name__icontains=query) |
                Q(site__site_name__icontains=query)
            ).distinct()
        return queryset

# 장소 목록
class LocationListView(ListView):
    model = Location
    template_name = 'api/location_list.html'
    context_object_name = 'locations'


# 장소별 콘서트 보기 HTML 페이지
class ConcertsByLocationView(ListView):
    model = Concert
    template_name = 'api/concerts_by_location.html'
    context_object_name = 'concerts'

    def get_queryset(self):
        location_id = self.kwargs.get('location_id')
        location = Location.objects.filter(location_id=location_id).first()

        if not location:
            raise NotFound("Location not found")
        # 'location_name'을 템플릿에 전달
        self.extra_context = {
            'location_name': location.location_name
        }

        return Concert.objects.filter(location=location)
    
    def get_context_data(self, **kwargs):
        # 부모 클래스에서 기본 컨텍스트 가져오기
        context = super().get_context_data(**kwargs)
        # 추가적인 데이터 추가 (location_name)
        context.update(self.extra_context)

        return context
    
# 검색 기능
class ConcertSearchView(APIView):
    queryset = Concert.objects.all()
    serializer_class = ConcertSerializer

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', None)
        concerts = []

        if query is not None:  # 'q' 파라미터가 있는 경우만 검색
            if query.strip() == "":
                concerts = []
            else:
                concerts = self.queryset.filter(
                    Q(title__icontains=query) |
                    Q(start_date__icontains=query) |
                    Q(end_date__icontains=query) |
                    Q(location__location_name__icontains=query) |
                    Q(site__site_name__icontains=query)
                )

        return render(request, 'api/search.html', {
            'concerts': concerts,
            'query': query
        })
