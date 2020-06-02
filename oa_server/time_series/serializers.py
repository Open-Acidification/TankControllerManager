from rest_framework import serializers
from time_series.models import TimeSeries

# Pylint wants create() and update() to be overriden,
# but we don't need them here, so ignore the error.
#pylint: disable=abstract-method
class TimeSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSeries
        fields = '__all__'

class TempHoldSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=32, default="Unnamed")
    at = serializers.FloatField(min_value=0, max_value=100, default=20)

class PHHoldSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=32, default="Unnamed")
    at = serializers.FloatField(min_value=7, max_value=14, default=8)

class TempRampSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=32, default="Unnamed")
    start = serializers.FloatField(min_value=0, max_value=100, default=20)
    end = serializers.FloatField(min_value=0, max_value=100, default=30)
    duration = serializers.IntegerField(min_value=0, default=600)

class PHRampSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=32, default="Unnamed")
    start = serializers.FloatField(min_value=7, max_value=14, default=8)
    end = serializers.FloatField(min_value=7, max_value=14, default=9)
    duration = serializers.IntegerField(min_value=0, default=600)

class TempSineSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=32, default="Unnamed")
    frequency = serializers.IntegerField(min_value=0, default=600)
    amplitude = serializers.FloatField(min_value=0, max_value=50, default=15)
    offset_x = serializers.IntegerField(min_value=0, default=0)
    offset_y = serializers.FloatField(min_value=0, max_value=100, default=30)

class PHSineSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=32, default="Unnamed")
    frequency = serializers.IntegerField(min_value=0, default=600)
    amplitude = serializers.FloatField(min_value=0, max_value=3.5, default=1)
    offset_x = serializers.IntegerField(min_value=0, default=0)
    offset_y = serializers.FloatField(min_value=7, max_value=14, default=8)
