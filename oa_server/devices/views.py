import csv
from datetime import datetime
import requests
import pytz
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.parsers import JSONParser
from rest_framework_csv.renderers import CSVRenderer
from django_q.tasks import schedule, result
from django_q.models import Schedule
from devices.models import Device, Datum
from devices.serializers import DeviceSerializer, DatumSerializer
from devices.utils import get_mac


@csrf_exempt
@require_http_methods(["GET", "POST"])
def device_list(request):
    # Save the specified device
    if request.method == 'POST':
        # Get the IP address. We'll verify its validity when we check the MAC
        address = request.POST.get('ip', default=None)

        # Get the MAC address, or return an error if the IP can't be reached
        try:
            mac = get_mac(address)

        except requests.exceptions.ConnectionError:
            return HttpResponse(f"The specified IP address {address} is invalid", status=421)
        except requests.exceptions.Timeout:
            return HttpResponse(f"The specified IP address {address}" + \
                " could not be reached in time", status=421)
        except ValueError as err:
            return HttpResponse(err, status=421)

        name = request.POST.get('name', default='Unnamed')
        notes = request.POST.get('notes', default='N/A')

        data = {'name': name, 'ip': address, 'mac': mac, 'notes': notes}

        device_serializer = DeviceSerializer(data=data)
        if device_serializer.is_valid():
            device = device_serializer.save()
            # Schedule a refresh every 15 minutes
            device.schedule = schedule('devices.views.scheduled_refresh', mac=mac, \
                schedule_type='I', minutes=15)
            device.save()
            return JsonResponse(device_serializer.data, status=201)
        return JsonResponse(device_serializer.errors, status=400)

    # Return a list of all devices (GET)
    devices = Device.objects.all()
    device_serializer = DeviceSerializer(devices, many=True)
    return JsonResponse(device_serializer.data, safe=False)

@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
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

@csrf_exempt
@require_http_methods(["GET"])
def manage_data(request, mac):
    # First, check if specified device exists
    try:
        device = Device.objects.get(mac=mac)
    except Device.DoesNotExist:
        return HttpResponse("There is no device with the specified MAC address.", status=404)


    ### Read the specified device's data (GET) ###

    # Query database #
    min_time = request.GET.get('start', default=pytz.utc.localize(datetime.min))
    max_time = request.GET.get('end', default=pytz.utc.localize(datetime.utcnow()))

    # Convert parameters to datetime if not already
    try:
        min_time = pytz.utc.localize(datetime.strptime(min_time, '%y%m%d_%H%M%S'))
    except TypeError:
        pass
    try:
        max_time = pytz.utc.localize(datetime.strptime(max_time, '%y%m%d_%H%M%S'))
    except TypeError:
        pass

    data = Datum.objects.\
        filter(device=device, time__range=[min_time, max_time]).order_by('time').values()

    response = HttpResponse(content_type='text/plain')

    download = int(request.GET.get('download', default=0))

    if download: # Download our file with a unique name
        response['Content-Disposition'] = 'attachment; filename=' + \
        '"device-'+mac+' start-'+min_time.strftime('%y%m%d_%H%M%S')+\
        ' end-'+max_time.strftime('%y%m%d_%H%M%S')+'.csv"'

    # Set up CSV writer
    fieldnames = ['time', 'tankid', 'temp', 'temp_setpoint', 'pH', \
        'pH_setpoint', 'on_time']
    writer = csv.DictWriter(response, fieldnames, extrasaction='ignore')

    # CSV Writing
    # Write custom header
    writer.writerow({'time':'time', 'tankid':'tankid', 'temp':'temp', \
        'temp_setpoint':'temp setpoint', 'pH':'pH', 'pH_setpoint':'pH setpoint', \
        'on_time':'onTime'})
    # Write data
    for datum in data:
        datum['time'] = datum['time'].strftime('%Y/%m/%d %H:%M:%S')
        writer.writerow(datum)

    return response

def scheduled_refresh(mac):
    """
    Wrapper for Device.scheduled_refresh(), allowing passing function as string
    """
    device = Device.objects.get(mac=mac)
    return device.scheduled_refresh()
