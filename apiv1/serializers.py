import datetime

from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from bmonster.models import Studio, Performer, Program, Schedule, AttendanceHistory

JST = datetime.timezone(datetime.timedelta(hours=9))


class StudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Studio
        exclude = ['created_datetime', 'modified_datetime']


class PerformerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performer
        exclude = ['created_datetime', 'modified_datetime']


class ProgramSerializer(serializers.ModelSerializer):
    performer = PerformerSerializer()

    class Meta:
        model = Program
        exclude = ['created_datetime', 'modified_datetime']


class ScheduleSerializer(serializers.ModelSerializer):
    studio = serializers.ReadOnlyField(source='studio.name')
    performer = serializers.ReadOnlyField(source='performer.name')
    program = serializers.ReadOnlyField(source='program.name')
    end_time = serializers.SerializerMethodField()

    class Meta:
        model = Schedule
        exclude = ['created_datetime', 'modified_datetime']

    def get_end_time(self, instance):
        return instance.start_time.astimezone(JST) + datetime.timedelta(minutes=45)


class AttendanceHistorySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=CurrentUserDefault())
    program = ProgramSerializer()

    class Meta:
        model = AttendanceHistory
        exclude = ['created_datetime', 'modified_datetime']
