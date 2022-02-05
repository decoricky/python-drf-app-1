from django_filters import rest_framework as filters
from rest_framework import generics, views, status
from rest_framework.response import Response

from .serializers import Studio, StudioSerializer

from bmonster import scraping


class UpdateDataAPIView(views.APIView):
    def post(self, request, *args, **kwargs):
        scraping.update_data()
        return Response(status=status.HTTP_201_CREATED)


class StudioListAPIView(generics.ListAPIView):
    queryset = Studio.objects.all()
    serializer_class = StudioSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['code', 'name']
