from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from allincon.models import Concert, Location
from .serializers import ConcertSerializer

class ConcertUploadView(APIView):
    def post(self, request):
        concerts=request.data
        for data in concerts:
            # 1. location name으로 Location 객체 가져오거나 새로 생성
            location_name = data.get('location')
            location_obj, _ = Location.objects.get_or_create(name=location_name)

            # 2. 복사 후 location을 id로 교체
            concert_data = data.copy()
            concert_data['location'] = location_obj.id

            # 3. serializer에 넣고 저장
            serializer = ConcertSerializer(data=concert_data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Concerts uploaded successfully"}, status=status.HTTP_201_CREATED)