from rest_framework import serializers
from devices.models import Device, Datum

class DeviceSerializer(serializers.ModelSerializer):
    online = serializers.ReadOnlyField()

    class Meta:
        model = Device
        fields = ['mac', 'name', 'ip', 'online', 'last_refreshed', 'notes']

class DatumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Datum
        fields = '__all__'
