from django_filters import rest_framework as filters
from rest_framework import generics, views, status
from rest_framework.response import Response

from bmonster import scraping
from bmonster.models import Studio, Performer, Program, Schedule
from .serializers import StudioSerializer, PerformerSerializer, ProgramSerializer, ScheduleSerializer


class UpdateDataAPIView(views.APIView):
    def post(self, request, *args, **kwargs):
        scraping.update_data()
        return Response(status=status.HTTP_201_CREATED)


class StudioListAPIView(generics.ListAPIView):
    queryset = Studio.objects.all()
    serializer_class = StudioSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['code', 'name']


class PerformerListAPIView(generics.ListAPIView):
    queryset = Performer.objects.all()
    serializer_class = PerformerSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['name']


class ProgramListAPIView(generics.ListAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['performer', 'name']


class ScheduleListAPIView(generics.ListAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['studio', 'performer', 'program']
