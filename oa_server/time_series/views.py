from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.parsers import JSONParser
from time_series.models import TimeSeries
from time_series.serializers import TimeSeriesSerializer, TempHoldSerializer, PHHoldSerializer, \
    TempRampSerializer, PHRampSerializer, TempSineSerializer, PHSineSerializer
from time_series.utils import point_in_wave, sanitize_ts_type, \
    hold_to_time_series, ramp_to_time_series, sine_to_time_series


@csrf_exempt
@require_http_methods(["GET"])
def time_series_list(request, ts_type=''):
    ts_type = sanitize_ts_type(ts_type)

    # Return a list of all time series of the specified parameter
    if ts_type == '':
        series = TimeSeries.objects.all()
    else:
        series = TimeSeries.objects.filter(type=ts_type)

    ts_serializer = TimeSeriesSerializer(series, many=True)
    return JsonResponse(ts_serializer.data, safe=False)

@csrf_exempt
@require_http_methods(["GET", "POST"])
def time_series_save(request):
    # Save the provided time series
    if request.method == 'POST':
        data = JSONParser().parse(request)
        ts_serializer = TimeSeriesSerializer(data=data)
        if ts_serializer.is_valid():
            ts_serializer.save()
            return JsonResponse(ts_serializer.data, status=201)
        return JsonResponse(ts_serializer.errors, status=400)

    # Return a list of all time series of the specified type (GET)
    return time_series_list(request)

@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def time_series_detail(request, time_series_id):
    # First, check if specified time series exists
    try:
        series = TimeSeries.objects.get(id=time_series_id)
    except TimeSeries.DoesNotExist:
        return HttpResponse(status=404)

    # Update the specified time series
    if request.method == 'PUT':
        data = JSONParser().parse(request)
        ts_serializer = TimeSeriesSerializer(series, data=data)
        if ts_serializer.is_valid():
            ts_serializer.save()
            return JsonResponse(ts_serializer.data)
        return JsonResponse(ts_serializer.errors, status=400)

    # Delete the specified time series
    if request.method == 'DELETE':
        series.delete()
        return HttpResponse(status=204)

    # Read the specified time series (GET)
    ts_serializer = TimeSeriesSerializer(series)
    return JsonResponse(ts_serializer.data)

@csrf_exempt
@require_http_methods(["GET", "POST"])
def time_series_generate_hold(request, ts_type=''):
    ts_type = sanitize_ts_type(ts_type)

    if not ts_type:
        return JsonResponse({'error': "Please specify /temp/ or /pH/"}, status=400)

    # Get our constraint parameters
    if request.method == 'POST':
        constraints = JSONParser().parse(request)
    else:
        constraints = request.GET

    # Validate based on the type of time series
    if ts_type == 'T':
        hold_serializer = TempHoldSerializer(data=constraints)
    else:
        hold_serializer = PHHoldSerializer(data=constraints)

    # Validate
    if hold_serializer.is_valid():
        constraints = hold_serializer.data
    else:
        return JsonResponse(hold_serializer.errors, status=400)

    # Get time series from constraints
    time_series = hold_to_time_series(constraints['at'])

    ### POST ###
    if request.method == 'POST':
        return post_time_series(time_series, constraints['name'], ts_type)

    ### GET ###
    return JsonResponse(time_series)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def time_series_generate_ramp(request, ts_type=''):
    ts_type = sanitize_ts_type(ts_type)

    if not ts_type:
        return JsonResponse({'error': "Please specify /temp/ or /pH/"}, status=400)

    # Get our constraint parameters
    if request.method == 'POST':
        constraints = JSONParser().parse(request)
    else:
        constraints = request.GET

    # Validate based on the type of time series
    if ts_type == 'T':
        ramp_serializer = TempRampSerializer(data=constraints)
    else:
        ramp_serializer = PHRampSerializer(data=constraints)

    # Validate
    if ramp_serializer.is_valid():
        constraints = ramp_serializer.data
    else:
        return JsonResponse(ramp_serializer.errors, status=400)

    # Get time series from constraints
    time_series = ramp_to_time_series(constraints['start'], constraints['end'],
                                      constraints['duration'])

    ### POST ###
    if request.method == 'POST':
        return post_time_series(time_series, constraints['name'], ts_type)

    ### GET ###
    return JsonResponse(time_series)

@csrf_exempt
@require_http_methods(["GET", "POST"])
def time_series_generate_sine(request, ts_type=''):
    ts_type = sanitize_ts_type(ts_type)

    if not ts_type:
        return JsonResponse({'error': "Please specify /temp/ or /pH/"}, status=400)

    # Get our constraint parameters
    if request.method == 'POST':
        constraints = JSONParser().parse(request)
    else:
        constraints = request.GET

    # Validate based on the type of time series
    if ts_type == 'T':
        sine_serializer = TempSineSerializer(data=constraints)
    else:
        sine_serializer = PHSineSerializer(data=constraints)

    # Validate
    if sine_serializer.is_valid():
        constraints = sine_serializer.data
    else:
        return JsonResponse(sine_serializer.errors, status=400)

    # Get time series from constraints
    time_series = sine_to_time_series(constraints['frequency'], constraints['amplitude'],
                                      constraints['offset_x'], constraints['offset_y'])

    ### POST ###
    if request.method == 'POST':
        return post_time_series(time_series, constraints['name'], ts_type)

    ### GET ###
    return JsonResponse(time_series)

def post_time_series(time_series, name, ts_type):
    # Add POST-specific fields
    time_series['name'] = name
    time_series['type'] = ts_type

    # Serialize the time series
    ts_serializer = TimeSeriesSerializer(data=time_series)
    if ts_serializer.is_valid():
        ts_serializer.save()
        return JsonResponse(ts_serializer.data, status=201)
    return JsonResponse(ts_serializer.errors, status=400)
