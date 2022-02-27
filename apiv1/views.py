import datetime

from django.utils.timezone import make_aware
from django_filters import rest_framework as filters
from rest_framework import generics, views, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import StudioSerializer, PerformerSerializer, ProgramSerializer, ScheduleSerializer, AttendanceHistorySerializer
from bmonster import models

TODAY = make_aware(datetime.datetime.now())
TODAY.replace(hour=0, minute=0, second=0, microsecond=0)


class UpdateDataAPIView(views.APIView):
    def post(self, request, *args, **kwargs):
        models.update_data()
        return Response(status=status.HTTP_201_CREATED)


class StudioListAPIView(generics.ListAPIView):
    queryset = models.Studio.objects.all()
    serializer_class = StudioSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['code', 'name']
    permission_classes = [AllowAny]


class PerformerListAPIView(generics.ListAPIView):
    queryset = models.Performer.objects.all()
    serializer_class = PerformerSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['name']
    permission_classes = [AllowAny]


class ProgramListAPIView(generics.ListAPIView):
    queryset = models.Program.objects.all()
    serializer_class = ProgramSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['performer', 'name']
    permission_classes = [AllowAny]


class ScheduleListAPIView(generics.ListAPIView):
    queryset = models.Schedule.objects.filter(modified_datetime__gte=TODAY)
    serializer_class = ScheduleSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['studio', 'performer', 'program']
    permission_classes = [AllowAny]


class AttendanceHistoryViewSet(viewsets.ModelViewSet):
    queryset = models.AttendanceHistory.objects.all()
    serializer_class = AttendanceHistorySerializer

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
