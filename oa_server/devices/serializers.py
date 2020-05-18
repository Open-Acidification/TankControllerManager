from rest_framework import serializers
from devices.models import Device, Datum

class DeviceSerializer(serializers.ModelSerializer):
    status = serializers.ReadOnlyField()

    class Meta:
        model = Device
        fields = ['mac', 'name', 'ip', 'status', 'notes']

class DatumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Datum
        fields = '__all__'
