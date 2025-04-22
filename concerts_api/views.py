from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
#from rest_framework.decorators import api_view
from concerts.models import Location, Concert, Site
from .serializers import ConcertListSerializer, ConcertWriteSerializer, VenueConcertCountSerializer

# @api_view()
# def concert_list(request):
#     concerts = Concert.objects.all()
#     serializer = ConcertSerializer(concerts, many = True)
#     return Response(serializer.data)

class ConcertListView(generics.ListAPIView):
    serializer_class = ConcertListSerializer
    def get_queryset(self):
        queryset = Concert.objects.select_related('location', 'source').all()
        location_name_param = self.request.query_params.get('location_name', None)
        month_param = self.request.query_params.get('month', None)

        if location_name_param:
            queryset = queryset.filter(location__name__icontains=location_name_param)

        if month_param:
            try:
                year, month = map(int, month_param.split('-'))
                queryset = queryset.filter(start_date__year=year, start_date__month=month)
            except (ValueError, TypeError):
                pass
        return queryset
        
class ConcertCrawlAPIView(APIView):
    def post(self, request):
        concert_data_list = request.data
        successful_uploads = 0
        failed_uploads = []
        skipped_duplicates = 0 
        for data in concert_data_list:
            location_name = data.get('location')
            site_name = data.get('source')
            title = data.get('title')
            start_date_str = data.get('start_date')

            location_obj = None
            if location_name and location_name.strip():
                location_obj, _ = Location.objects.get_or_create(name=location_name.strip())

            site_obj = None
            if site_name and site_name.strip():
                site_obj, _ = Site.objects.get_or_create(name=site_name.strip())

            serializer_data = {
                'title': title,
                'location': location_obj.id if location_obj else None, 
                'source': site_obj.id if site_obj else None,      
                'start_date': start_date_str,
                'end_date': data.get('end_date'),
                }
            
            unique_check_data = {
                'title': title,
                'location': location_obj,
                'start_date_str': start_date_str
            }

            parsed_start_date = None
            if start_date_str:
                parsed_start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            concert_exists = Concert.objects.filter(
                title=unique_check_data['title'],
                location=unique_check_data['location'],
                start_date=parsed_start_date
            ).exists()
            if concert_exists:
                skipped_duplicates += 1
                continue

            serializer = ConcertWriteSerializer(data=serializer_data)
            if serializer.is_valid(raise_exception=False):
                serializer.save()
                successful_uploads += 1
            else:
                failed_uploads.append({
                    "input_data": data, 
                    "errors": serializer.errors
                })
            
        response_data = {
            "message": "데이터 처리가 완료되었습니다.",
            "total_received": len(concert_data_list),
            "successful_uploads": successful_uploads,
            "failed_uploads": failed_uploads,
            "failed_count": len(failed_uploads)
        }
        if failed_uploads:
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(response_data, status=status.HTTP_201_CREATED)
        
class VenueConcertCountView(APIView):
    def get(self, request):
        venue_counts = Location.objects.annotate(
            concert_count=Count('concerts')
        ).filter(
            concert_count__gt=0
        ).values(
            'name', 'concert_count'
        ).order_by('-concert_count', 'name')

        serializer = VenueConcertCountSerializer(venue_counts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)