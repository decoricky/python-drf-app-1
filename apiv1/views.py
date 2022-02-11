import datetime

from django_filters import rest_framework as filters
from rest_framework import generics, views, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import StudioSerializer, PerformerSerializer, ProgramSerializer, ScheduleSerializer, AttendanceHistorySerializer
from bmonster import scraping
from bmonster.models import Studio, Performer, Program, Schedule, AttendanceHistory

JST = datetime.timezone(datetime.timedelta(hours=9))
TODAY = datetime.datetime.now(JST).date()


class UpdateDataAPIView(views.APIView):
    def post(self, request, *args, **kwargs):
        scraping.update_data()
        return Response(status=status.HTTP_201_CREATED)


class StudioListAPIView(generics.ListAPIView):
    queryset = Studio.objects.all()
    serializer_class = StudioSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['code', 'name']
    permission_classes = [AllowAny]


class PerformerListAPIView(generics.ListAPIView):
    queryset = Performer.objects.all()
    serializer_class = PerformerSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['name']
    permission_classes = [AllowAny]


class ProgramListAPIView(generics.ListAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['performer', 'name']
    permission_classes = [AllowAny]


class ScheduleListAPIView(generics.ListAPIView):
    queryset = Schedule.objects.filter(modified_datetime__gte=TODAY)
    serializer_class = ScheduleSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['studio', 'performer', 'program']
    permission_classes = [AllowAny]


class AttendanceHistoryViewSet(viewsets.ModelViewSet):
    queryset = AttendanceHistory.objects.all()
    serializer_class = AttendanceHistorySerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['user']
