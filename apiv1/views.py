from django_filters import rest_framework as filters
from rest_framework import generics

from .serializers import Studio, StudioSerializer


class StudioListAPIView(generics.ListAPIView):
    queryset = Studio.objects.all()
    serializer_class = StudioSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['code', 'name']
