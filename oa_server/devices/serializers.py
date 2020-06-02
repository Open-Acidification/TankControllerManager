from rest_framework import serializers
from devices.models import Device, Datum

class DeviceSerializer(serializers.ModelSerializer):
    status = serializers.ReadOnlyField()
    current_tank = serializers.ReadOnlyField()

    class Meta:
        model = Device
        fields = ['mac', 'name', 'ip', 'status', 'current_tank',
                  'ph_variance', 'temp_variance', 'notes']

class DatumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Datum
        fields = '__all__'
