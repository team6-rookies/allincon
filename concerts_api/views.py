from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
#from rest_framework.decorators import api_view
from concerts.models import Location, Concert, Site
from .serializers import ConcertSerializer

# @api_view()
# def concert_list(request):
#     concerts = Concert.objects.all()
#     serializer = ConcertSerializer(concerts, many = True)
#     return Response(serializer.data)

class ConcertCrawlAPIView(APIView):
    def post(self, request):
        concert_data_list = request.data
        successful_uploads = 0
        failed_uploads = []
        for data in concert_data_list:
            location_name = data.get('location')
            site_name = data.get('source')
            location_obj = None
            if location_name and location_name.strip():
                location_obj, _ = Location.objects.get_or_create(name=location_name.strip())

            site_obj = None
            if site_name and site_name.strip():
                site_obj, _ = Site.objects.get_or_create(name=site_name.strip())

            serializer_data = {
                'title': data.get('title'),
                'location': location_obj.id if location_obj else None, 
                'source': site_obj.id if site_obj else None,      
                'start_date': data.get('start_date'),
                'end_date': data.get('end_date'),
                }
            
            serializer = ConcertSerializer(data=serializer_data)
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