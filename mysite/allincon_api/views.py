from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from allincon.models import *
from .serializers import *
from django.db.models.functions import TruncMonth
from django.db.models import Count
#좀더 restful하게 바꿔보자

class ConcertListView(APIView):
    #전체 콘서트 리스트 조회, 검색 기능에 사용된다.
    def get(self, request):
        query = request.GET.get('query', '') # 사용자가 사용한 쿼리문을 가져온다.
        search_type = request.GET.get('search_type', '')  # 'title' 또는 'location'

        if search_type == 'title': # title concert 검색
            concerts = Concert.objects.filter(title__icontains=query)
            serializer = ConcertSerializer(concerts, many=True)
            return render(request, 'allincon/index.html', {'concerts': serializer.data})

        elif search_type == 'location': # location concert 검색
            concerts = Concert.objects.filter(location__name__icontains=query)
            serializer = ConcertSerializer(concerts, many=True)
            return render(request, 'allincon/index.html', {'concerts': serializer.data})
        else: # 기본적으로 모든 concert 검색
            concerts = Concert.objects.all()
            serializer = ConcertSerializer(concerts, many=True)
            return render(request,'allincon/all_in_one_app.html',{'concerts': serializer.data})

        #애초에 프론트 백이 나눠져 있지않아서 그냥 서버에서 바로 보여주기위해서 rendering한다.
        # 만약 restful하게 할거면 Response로 보내주고 프론트에서 ajax로 받아서 처리해야함. js파일 이용용
        #return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        concerts=request.data
        for data in concerts:
            # 1. 중복된 title이 있는 경우 저장 생략
            title = data.get('title')
            if Concert.objects.filter(title=title).exists():
                continue

            # 2. location name으로 Location 객체 가져오거나 새로 생성
            location_name = data.get('location')
            location_obj, _ = Location.objects.get_or_create(name=location_name)

            # 3. site name으로 Site 객체 가져오거나 새로 생성
            site_name = data.get('site')
            site_obj, _ = Site.objects.get_or_create(name=site_name)

            # 4. 직렬화된 데이터에 location과 site를 해당 객체로 넣기
            concert_data = data.copy()  # 데이터 복사
            concert_data['location'] = location_obj.id  # 외래키 ID로 설정 전달받은건 그냥 장소명이니까 
            concert_data['site'] = site_obj.id  # 외래키 ID로 설정

            # 5. serializer에 넣고 저장
            serializer = ConcertSerializer(data=concert_data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Concerts uploaded successfully"}, status=status.HTTP_201_CREATED)    
    
class LocationListView(APIView):
    #전체 location 리스트 조회에 사용된다. 
    def get(self, request):
        locations = Location.objects.annotate(concert_count=models.Count('concert'))    
        #location에 저장된 모든 location을 가져옴과 동시에 각 location에 해당하는 concert의 개수를 가져옴(foreignkey로 연결된 concert의 개수)

        # 현재 시간 이후의 가장 가까운 콘서트를 가져오는 로직
        now = timezone.now() # 현재 시간
        location_data = []

        for location in locations:
            # 각 location에 해당하는 콘서트 개수 가져오기
            #concert_count = location.concert_set.count()  # 각 Location의 콘서트 수 계산
            location_dict = LocationSerializer(location).data
            location_dict['concert_count'] = location.concert_count

            # 가장 가까운 콘서트 가져오기 (start_date가 현재 시간 이후인 것 중 가장 가까운)
            closest_concert = Concert.objects.filter(
                location=location,
                start_date__gte=now
            ).order_by('start_date').first()

            location_data.append({
                'location': location,
                'concert_count': location.concert_count,
                'closest_concert': closest_concert
            })

        serializer = LocationDataSerializer(location_data, many=True)
        print(serializer.data)
        return render(request, 'allincon/location_agg_app.html',{'locations': serializer.data})

    def post(self, request):
        concerts=request.data
        serializer = ConcertSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ConcertByLocationView(APIView):
    
    #특정 Location의 Concert 목록 조회에 사용된다.
    def get(self, request, location_id):
        concerts = Concert.objects.filter(location_id=location_id)
        location= Location.objects.get(id=location_id)
        serializer = ConcertSerializer(concerts, many=True)
        serializer_location = LocationSerializer(location)
    
        #return Response(serializer.data)
        return render(request, 'allincon/location_group_app.html', {'concerts': serializer.data,'location': serializer_location.data})


class ConcertMonthView(APIView):
    def get(self, request):
        # 월별로 콘서트 수와 제목 가져오기
        monthly_concerts = Concert.objects.annotate(
            month=TruncMonth('start_date')
        ).values('month').annotate(
            count=Count('id'),
            titles=Count('title')  # 월별로 제목의 개수를 카운트
        ).order_by('month')

        # 월별 콘서트 수 및 제목 리스트 생성
        monthly_data = []
        for entry in monthly_concerts:
            month_str = entry['month'].strftime('%Y-%m')  # 예: '2025-04'
            concerts_in_month = Concert.objects.filter(
                start_date__year=entry['month'].year,
                start_date__month=entry['month'].month
            )
            concert_titles = [concert.title for concert in concerts_in_month]
            
            monthly_data.append({
                'month': month_str,
                'count': entry['count'],
                'concert_titles': concert_titles
            })

        return render(request, 'allincon/monthly_concerts.html', {'monthly_data': monthly_data})





















# class ConcertCreateView(APIView):
#     def post(self, request):
#         concerts=request.data
#         for data in concerts:
#             # 1. 중복된 title이 있는 경우 저장 생략
#             title = data.get('title')
#             if Concert.objects.filter(title=title).exists():
#                 continue

#             # 2. location name으로 Location 객체 가져오거나 새로 생성
#             location_name = data.get('location')
#             location_obj, _ = Location.objects.get_or_create(name=location_name)

#             # 3. 복사 후 location을 id로 교체
#             concert_data = data.copy()
#             concert_data['location'] = location_obj.id

#             # 4. site name으로 Site 객체 가져오거나 새로 생성
#             site_name = data.get('site')
#             site_obj, _ = Site.objects.get_or_create(name=site_name)
#             concert_data['site'] = site_obj.id

#             # 5. serializer에 넣고 저장
#             serializer = ConcertSerializer(data=concert_data)
#             if serializer.is_valid():
#                 serializer.save()
#             else:
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         return Response({"message": "Concerts uploaded successfully"}, status=status.HTTP_201_CREATED)
    

# def search_concerts(request):
#     query = request.GET.get('query', '')
#     search_type = request.GET.get('search_type')

#     concerts = []

#     if search_type == 'title' and query:
#         concerts = Concert.objects.filter(title__icontains=query)
#     elif search_type == 'location' and query:
#         concerts = Concert.objects.filter(location__name__icontains=query)

#     return render(request, 'allincon/index.html', {'concerts': concerts})