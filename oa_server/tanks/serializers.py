from rest_framework import serializers

class TankHistorySerializer(serializers.Serializer):
    time = serializers.DateTimeField(format='%Y/%m/%d %H:%M:%S')
    mac = serializers.CharField(max_length=17)