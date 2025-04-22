from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from concerts.models import Concert
from rest_framework import generics
from .serializers import ConcertSerializer


class ConcertListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        region = request.GET.get('region')
        month = request.GET.get('month')
        title = request.GET.get('title')

        concerts = Concert.objects.all()

        if region:
            concerts = concerts.filter(location__name__icontains=region)
        if month:
            concerts = concerts.filter(start_date__month=month)
        if title:
            concerts = concerts.filter(title__icontains=title)

        serializer = ConcertSerializer(concerts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
