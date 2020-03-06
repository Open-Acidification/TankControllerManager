from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from devices.models import Device
from devices.serializers import DeviceSerializer
import os


@csrf_exempt
def device_list(request):
    # Return a list of all devices
    if request.method == 'GET':
        devices = Device.objects.all()
        serializer = DeviceSerializer(devices, many=True)
        return JsonResponse(serializer.data, safe=False)

    # Save the specified device
    elif request.method == 'POST':
        name = request.POST.get('name', default='Unnamed')
        ip = request.POST.__getitem__('ip')
        mac = '000000000001' # TODO: Get this information from the device.
        notes = request.POST.get('notes', default='N/A')

        data = {'name': name, 'ip': ip, 'mac': mac, 'notes': notes}

        # If the directory doesn't exist, create it
        try:
            os.mkdir(os.getcwd()+'/data/'+mac)
        except FileExistsError:
            pass



        serializer = DeviceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


def device_detail(request, mac):
    # First, check if specified device exists
    try:
        device = Device.objects.get(mac=mac)
    except Device.DoesNotExist:
        return HttpResponse(status=404)
    
    # Read the specified device
    if request.method == 'GET':
        serializer = DeviceSerializer(device)
        return JsonResponse(serializer.data)

    # Update the specified time series
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = DeviceSerializer(device, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    # Delete the specified time series
    elif request.method == 'DELETE':
        device.delete()
        return HttpResponse(status=204)