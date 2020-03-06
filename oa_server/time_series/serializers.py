from rest_framework import serializers
from time_series.models import TimeSeries

class TimeSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSeries
        fields = ['id', 'name', 'value', 'time', 'notes']