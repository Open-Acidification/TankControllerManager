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
from devices.utils import get_mac, strip_mac


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
        return HttpResponse("There is no device with the specified MAC address.", status=404)

    # Update the specified device
    if request.method == 'PUT':
        data = JSONParser().parse(request)
        data['mac'] = mac
        device_serializer = DeviceSerializer(device, data=data)
        if device_serializer.is_valid():
            device_serializer.save()
            return JsonResponse(device_serializer.data)
        return JsonResponse(device_serializer.errors, status=400)

    # Delete the specified device
    if request.method == 'DELETE':
        if device.schedule is None:
            device.delete()
        else:
            # This will conveniently delete both the device and its
            # schedule, since on_delete is set to CASCADE
            device.schedule.delete()
        return HttpResponse(status=204)

    # Read the specified device (GET)
    device_serializer = DeviceSerializer(device)
    return JsonResponse(device_serializer.data)

@csrf_exempt
@require_http_methods(["GET"])
def get_device_data(request, mac):
    """
    Queries data from the specified device according to constraints specified in the request.

    Returns the data as a CSV file.
    """
    # First, check if specified device exists
    try:
        device = Device.objects.get(mac=mac)
    except Device.DoesNotExist:
        return HttpResponse("There is no device with the specified MAC address.", status=404)

    constraints = get_constraints(request)

    data = query_data(constraints, device=device)

    download = bool(request.GET.get('download', default=False))
    show_device = bool(request.GET.get('showDevice', default=False))

    return create_csv(data, download, 'device-'+strip_mac(mac), show_device)

def get_constraints(request):
    """
    Returns a dictionary of all the constraints to be imposed on the returned data
    """
    ## Time constraints ##
    start = request.GET.get('start', default=pytz.utc.localize(datetime.min))
    end = request.GET.get('end', default=pytz.utc.localize(datetime.utcnow()))

    # Convert parameters to datetime if not already
    try:
        start = pytz.utc.localize(datetime.strptime(start, '%y%m%d%H%M%S'))
    except TypeError:
        pass
    try:
        end = pytz.utc.localize(datetime.strptime(end, '%y%m%d%H%M%S'))
    except TypeError:
        pass

    ## Number constraints ##
    freq = abs(int(request.GET.get('freq', default=0))) # Implementation currently unknown
    cutoff = int(request.GET.get('cutoff', default=0))
    total = abs(int(request.GET.get('total', default=0)))

    return {'start': start, 'end': end, 'freq': freq, 'cutoff': cutoff, 'total': total}

def query_data(constraints, **kwargs):
    """
    Queries data from the specified device according to the specified constraints.

    Returns the data as a list of dictionaries.
    """
    # Run the query with the specified time constraints and any additional keyword arguments
    data = list(Datum.objects.filter(**kwargs, \
        time__range=[constraints['start'], constraints['end']]).order_by('time').values())


    # There's no good way to accomplish these with Django queries, so let's just
    # take a small performance hit and do them manually

    if constraints['freq']:
        data = data[-1:0:-constraints['freq']]
        data.reverse()

    if constraints['cutoff']:
        if constraints['cutoff'] < 0:
            data = data[constraints['cutoff']:]
        else:
            data = data[:constraints['cutoff']]

    if constraints['total']:
        row_count = len(data)
        step = row_count // constraints['total']
        data = data[-1:0:-step]
        data.reverse()

    return data

def create_csv(data, download=False, identifier="", show_device=False):
    """
    Creates and returns a CSV from the given data.

    If download=True, the browser downloads the CSV file instead of rendering it.
    """
    response = HttpResponse(content_type='text/plain')

    start = data[0]['time']
    end = data[-1]['time']

    if download: # Download our file with a unique name
        response['Content-Disposition'] = 'attachment; filename=' + \
        '"'+identifier+'_start-'+start.strftime('%y%m%d%H%M%S')+\
        '_end-'+end.strftime('%y%m%d%H%M%S')+'.csv"'

    # Set up CSV writer
    fieldnames = ['time', 'tankid', 'temp', 'temp_setpoint', 'pH', \
        'pH_setpoint', 'on_time']
    writer = csv.DictWriter(response, fieldnames, extrasaction='ignore')

    # CSV Writing
    # Write custom header
    header = {'time':'time', 'tankid':'tankid', 'temp':'temp', \
        'temp_setpoint':'temp setpoint', 'pH':'pH', 'pH_setpoint':'pH setpoint', \
        'on_time':'onTime'}
    if show_device:
        fieldnames.append('device_id')
        header['device_id'] = 'device'
    writer.writerow(header)

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
