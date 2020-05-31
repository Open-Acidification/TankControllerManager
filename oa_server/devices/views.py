import csv
from datetime import datetime
import requests
import pytz
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from rest_framework.parsers import JSONParser
from rest_framework_csv.renderers import CSVRenderer
from django_q.tasks import schedule, result
from django_q.models import Schedule
from devices.models import Device, Datum
from devices.serializers import DeviceSerializer, DatumSerializer
from devices.utils import get_mac, strip_mac
from time_series.models import TimeSeries


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
    end = request.GET.get('end', default=timezone.now())

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
    freq = abs(int(request.GET.get('freq', default=0)))
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

@csrf_exempt
@require_http_methods(["GET", "POST"])
def manage_device_time_series(request, mac):
    # First, check if specified device exists
    try:
        device = Device.objects.get(mac=mac)
    except Device.DoesNotExist:
        return HttpResponse("There is no device with the specified MAC address.", status=404)

    if device.status != 1:
        return HttpResponse(f"The device with MAC address {device.mac} is offline.", status=421)


    if request.method == "GET":
        return get_device_time_series(request, device.ip)

    return post_device_time_series(request, device.ip)

def get_device_time_series(request, device_ip):
    try:
        response = requests.get(f"http://{device_ip}/series", timeout=5)
        response.raise_for_status()
        return JsonResponse(response.json, status=200)
    except requests.RequestException:
        return HttpResponse("An error occured when attempting to request the time series.", \
            status=400)

def post_device_time_series(request, device_ip):
    # If raw JSON provided, pass it directly to the device.
    raw_json = request.body.decode('utf-8')
    if raw_json[0] == '{':
        try:
            response = requests.post(f"http://{device_ip}/series", data=request.body, timeout=5)
            response.raise_for_status()

            # Actually, pylint, this is the correct way to go about this,
            # since we're returning raw (unserialized) JSON
            #pylint: disable=http-response-with-content-type-json
            message = HttpResponse(request.body, content_type='application/json', status=200)
        except requests.RequestException:
            message = HttpResponse("An error occured when attempting to upload time series.", \
                status=400)
        return message

    # Otherwise, use time series IDs specified in form data
    ts_params = get_time_series_form_data(request)

    if ts_params['error'] is not None:
        return ts_params['error']

    # Create the object containing both time series
    time_series = {
        'pH': {
            'value': ts_params['ph_ts'].value,
            'time': ts_params['ph_ts'].time,
            'interval': ts_params['ph_ts'].interval,
            'delay': ts_params['ph_delay']
        },
        'temp': {
            'value': ts_params['temp_ts'].value,
            'time': ts_params['temp_ts'].time,
            'interval': ts_params['temp_ts'].interval,
            'delay': ts_params['temp_delay']
        }
    }

    # Post the time series object to the device
    try:
        response = requests.post(f"http://{device_ip}/series", json=time_series, timeout=5)
        response.raise_for_status()
        return JsonResponse(time_series, status=200)
    except requests.RequestException:
        return HttpResponse("An error occured when attempting to upload time series.", status=400)

def get_time_series_form_data(request):
    error = None
    try:
        ph_id = int(request.POST.__getitem__('ph_id'))
        ph_ts = TimeSeries.objects.get(id=ph_id, type='P')
    except KeyError:
        error = HttpResponse("You must specify ph_id.", status=400)
    except ValueError:
        error = HttpResponse("ph_id must be an integer.", status=400)
    except TimeSeries.DoesNotExist:
        error = HttpResponse("There is no pH time series with the specified ID.", status=404)
    if error is not None:
        return {'error': error}

    try:
        temp_id = int(request.POST.__getitem__('temp_id'))
        temp_ts = TimeSeries.objects.get(id=temp_id, type='T')
    except KeyError:
        error = HttpResponse("You must specify temp_id.", status=400)
    except ValueError:
        error = HttpResponse("temp_id must be an integer.", status=400)
    except TimeSeries.DoesNotExist:
        error = HttpResponse("There is no temp time series with the specified ID.", status=404)
    if error is not None:
        return {'error': error}

    try:
        ph_delay = int(request.POST.get('ph_delay', default=0))
    except ValueError:
        error = HttpResponse("ph_delay must be an integer.", status=400)
        return {'error': error}

    try:
        temp_delay = int(request.POST.get('temp_delay', default=0))
    except ValueError:
        error = HttpResponse("temp_delay must be an integer.", status=400)
        return {'error': error}

    return {'ph_ts': ph_ts, 'ph_delay': ph_delay, 'temp_ts': temp_ts, 'temp_delay': temp_delay, \
        'error': error}

def scheduled_refresh(mac):
    """
    Wrapper for Device.scheduled_refresh(), allowing passing function as string
    """
    device = Device.objects.get(mac=mac)
    return device.scheduled_refresh()
