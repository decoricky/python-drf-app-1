from rest_framework import serializers

from bmonster.models import Studio, Performer, Program, Schedule


class StudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Studio
        exclude = ['created_datetime', 'modified_datetime']


class PerformerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performer
        exclude = ['created_datetime', 'modified_datetime']


class ProgramSerializer(serializers.ModelSerializer):
    performer_name = serializers.ReadOnlyField(source='performer.name')

    class Meta:
        model = Program
        fields = ['id', 'performer_name', 'name']


class ScheduleSerializer(serializers.ModelSerializer):
    studio_name = serializers.ReadOnlyField(source='studio.name')
    performer_name = serializers.ReadOnlyField(source='performer.name')
    program_name = serializers.ReadOnlyField(source='program.name')

    class Meta:
        model = Schedule
        fields = ['id', 'studio_name', 'start_time', 'performer_name', 'program_name']
