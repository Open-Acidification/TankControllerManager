from django.utils import timezone
from rest_framework import serializers
from devices.models import Device, Datum

# Pylint wants create() and update() to be overriden,
# but we don't need them here, so ignore the error.
# Also, Pylint isn't aware of Django REST Frameworks' requirement
# that SerializerMethodFields MUST be methods, not functions
#pylint: disable=abstract-method, no-self-use
class TankHistorySerializer(serializers.Serializer):
    time = serializers.DateTimeField()
    mac = serializers.CharField(max_length=17)

class TankSparklineDataSerializer(serializers.Serializer):
    time = serializers.ListField(child=serializers.DateTimeField(), required=False)
    temp = serializers.ListField(child=serializers.FloatField())
    pH = serializers.ListField(child=serializers.FloatField())

class TankSparklineSerializer(serializers.Serializer):
    tankid = serializers.IntegerField()
    sparklines = TankSparklineDataSerializer()
    error = serializers.CharField(required=False)

class TankStatusSerializer(serializers.ModelSerializer):
    last_update = serializers.DateTimeField(source='time')
    minutes_ago = serializers.SerializerMethodField()
    device_name = serializers.SerializerMethodField()
    device_mac = serializers.SerializerMethodField()
    temp_danger = serializers.SerializerMethodField()
    pH_danger = serializers.SerializerMethodField()

    class Meta:
        model = Datum
        fields = ['tankid', 'last_update', 'minutes_ago', 'temp', 'temp_setpoint', 'temp_danger', \
            'pH', 'pH_setpoint', 'pH_danger', 'on_time', 'device_name', 'device_mac']

    def get_minutes_ago(self, obj):
        difference = timezone.now() - obj.time
        return difference.seconds // 60

    def get_device_name(self, obj):
        return obj.device.name

    def get_device_mac(self, obj):
        return obj.device.mac

    def get_temp_danger(self, obj):
        return obj.get_temp_deviation()

    # In this specific case, we're going to ignore snake casing
    #pylint: disable=invalid-name
    def get_pH_danger(self, obj):
        return obj.get_ph_deviation()
