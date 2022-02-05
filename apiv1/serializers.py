from rest_framework import serializers

from bmonster.models import Studio


class StudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Studio
        fields = ['code', 'name']
        # exclude = ['id', 'created_datetime', 'modified_datetime']
