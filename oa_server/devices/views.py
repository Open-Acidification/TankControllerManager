import os
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.parsers import JSONParser
from devices.models import Device
from devices.serializers import DeviceSerializer


@csrf_exempt
@require_http_methods(["GET", "POST"])
def device_list(request):
    # Save the specified device
    if request.method == 'POST':
        name = request.POST.get('name', default='Unnamed')
        address = request.POST.__getitem__('ip')
        mac = '000000000001' # TODO: Get this information from the device.
        notes = request.POST.get('notes', default='N/A')

        data = {'name': name, 'ip': address, 'mac': mac, 'notes': notes}

        # If the directory doesn't exist, create it
        try:
            os.mkdir(os.getcwd()+'/data/'+mac)
        except FileExistsError:
            pass

        device_serializer = DeviceSerializer(data=data)
        if device_serializer.is_valid():
            device_serializer.save()
            return JsonResponse(device_serializer.data, status=201)
        return JsonResponse(device_serializer.errors, status=400)

    # Return a list of all devices (GET)
    devices = Device.objects.all()
    device_serializer = DeviceSerializer(devices, many=True)
    return JsonResponse(device_serializer.data, safe=False)


def device_detail(request, mac):
    # First, check if specified device exists
    try:
        device = Device.objects.get(mac=mac)
    except Device.DoesNotExist:
        return HttpResponse(status=404)

    # Update the specified time series
    if request.method == 'PUT':
        data = JSONParser().parse(request)
        device_serializer = DeviceSerializer(device, data=data)
        if device_serializer.is_valid():
            device_serializer.save()
            return JsonResponse(device_serializer.data)
        return JsonResponse(device_serializer.errors, status=400)

    # Delete the specified time series
    if request.method == 'DELETE':
        device.delete()
        return HttpResponse(status=204)

    # Read the specified device (GET)
    device_serializer = DeviceSerializer(device)
    return JsonResponse(device_serializer.data)
