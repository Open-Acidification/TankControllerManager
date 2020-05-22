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

class TankStatusSerializer(serializers.ModelSerializer):
    last_update = serializers.DateTimeField(source='time')
    device_name = serializers.SerializerMethodField()
    device_mac = serializers.SerializerMethodField()

    class Meta:
        model = Datum
        fields = ['tankid', 'last_update', 'temp', 'temp_setpoint', 'pH', \
            'pH_setpoint', 'on_time', 'device_name', 'device_mac']

    def get_device_name(self, obj):
        return obj.device.name

    def get_device_mac(self, obj):
        return obj.device.mac
