from rest_framework import generics, permissions, filters
from rest_framework.decorators import api_view
from .serializers import LocationSerializer, ConcertSerializer, SiteSerializer
from concerts.models import Location, Concert, Site

# @api_view()
# def concert_list(request):
#     concerts = Concert.objects.all()
#     serializer = ConcertSerializer(concerts, many = True)
#     return Response(serializer.data)

class LocationListAPIView(generics.ListAPIView):
    """ Location 목록 조회 API (GET) """
    queryset = Location.objects.all().order_by('name')
    serializer_class = LocationSerializer
    permission_classes = [permissions.AllowAny]
    # 검색 기능 유지 (선택 사항)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class LocationRetrieveAPIView(generics.RetrieveAPIView):
    """ Location 상세 조회 API (GET) """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [permissions.AllowAny]
    # lookup_field = 'pk' # 기본값이 pk 이므로 생략 가능

# --- Site Views ---
class SiteListAPIView(generics.ListAPIView):
    """ Site 목록 조회 API (GET) """
    queryset = Site.objects.all().order_by('name')
    serializer_class = SiteSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class SiteRetrieveAPIView(generics.RetrieveAPIView):
    """ Site 상세 조회 API (GET) """
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
    permission_classes = [permissions.AllowAny]

# --- Concert Views ---
class ConcertListAPIView(generics.ListAPIView):
    """ Concert 목록 조회 API (GET) """
    queryset = Concert.objects.all().order_by('start_date', 'title')
    serializer_class = ConcertSerializer
    permission_classes = [permissions.AllowAny]
    # 검색 기능 유지 (선택 사항)
    filter_backends = [filters.SearchFilter] # 필요하면 DjangoFilterBackend 등 추가
    search_fields = ['title', 'location__name', 'source__name'] # 검색 필드 확장

class ConcertRetrieveAPIView(generics.RetrieveAPIView):
    """ Concert 상세 조회 API (GET) """
    queryset = Concert.objects.all()
    serializer_class = ConcertSerializer
    permission_classes = [permissions.AllowAny]

# --- (선택 사항) 특정 Location 의 콘서트 목록 API ---
class ConcertsByLocationAPIView(generics.ListAPIView):
    """ 특정 Location ID에 해당하는 Concert 목록 조회 API (GET) """
    serializer_class = ConcertSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """ URL에서 location_pk를 받아 해당 location의 콘서트만 필터링 """
        location_pk = self.kwargs['location_pk'] # URL 파라미터 가져오기
        return Concert.objects.filter(location__pk=location_pk).order_by('start_date', 'title')

# --- (선택 사항) 특정 Site 의 콘서트 목록 API ---
class ConcertsBySiteAPIView(generics.ListAPIView):
    """ 특정 Site ID에 해당하는 Concert 목록 조회 API (GET) """
    serializer_class = ConcertSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """ URL에서 source_pk를 받아 해당 source의 콘서트만 필터링 """
        source_pk = self.kwargs['source_pk'] # URL 파라미터 가져오기
        return Concert.objects.filter(source__pk=source_pk).order_by('start_date', 'title')