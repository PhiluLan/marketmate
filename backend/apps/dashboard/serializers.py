from rest_framework import serializers
from .models import Metric, CalendarEvent

class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = ['id', 'type', 'value', 'date']

class CalendarEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarEvent
        fields = '__all__'
        read_only_fields = ['user']
