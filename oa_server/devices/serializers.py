from rest_framework import serializers
from devices.models import Device, Datum

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'

class DatumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Datum
        fields = '__all__'
