from rest_framework import serializers

# Pylint wants create() and update() to be overriden,
# but we don't need them here, so ignore the error.
#pylint: disable=abstract-method
class TankHistorySerializer(serializers.Serializer):
    time = serializers.DateTimeField(format='%Y/%m/%d %H:%M:%S')
    mac = serializers.CharField(max_length=17)
