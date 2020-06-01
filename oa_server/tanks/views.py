from datetime import datetime
import pytz
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, JsonResponse
from django.db import connection
from django.utils import timezone
from tanks.serializers import TankHistorySerializer, TankStatusSerializer, TankSparklineSerializer
from devices.models import Device, Datum
from devices.serializers import DatumSerializer
from devices.views import get_constraints, query_data, create_csv

@require_http_methods(["GET"])
def get_tanks(request):
    """
    Returns a list of all tanks and their status, each with its most recent device.
    """
    tanks = Datum.objects.order_by('tankid', '-time').distinct('tankid')
    status_serializer = TankStatusSerializer(tanks, many=True)
    return JsonResponse(status_serializer.data, safe=False)

@csrf_exempt
@require_http_methods(["GET", "DELETE"])
def manage_tank(request, tankid):
    """
    Wrapper for tank GET and DELETE requests
    """
    if request.method == 'GET':
        return get_tank(tankid)

    # if request.method == 'DELETE':
    return delete_tank(tankid)

def get_tank(tankid):
    """
    Returns the status of the specified tank, along with its most recent device.
    """
    tank = Datum.objects.filter(tankid=tankid).order_by('-time')[0]
    if tank is None:
        return HttpResponse("There is no tank with the specified ID.", status=404)

    status_serializer = TankStatusSerializer(tank)
    return JsonResponse(status_serializer.data, safe=False)

def delete_tank(tankid):
    """
    Deletes all data from the specified tank.
    """
    Datum.objects.filter(tankid=tankid).delete()
    return HttpResponse(status=204)

@require_http_methods(["GET"])
def get_tank_data(request, tankid):
    """
    Queries data from the specified tank ID according to constraints specified in the request.

    Returns the data as a CSV file.
    """
    constraints = get_constraints(request)

    data = query_data(constraints, tankid=tankid)

    download = bool(request.GET.get('download', default=False))
    show_device = bool(request.GET.get('showDevice', default=False))

    return create_csv(data, download, 'tankid-'+tankid, show_device)

@require_http_methods(["GET"])
def get_tank_history(request, tankid):
    """
    Returns a response listing the device history for each tank.
    """
    # Sanitize tankid
    tankid = int(tankid)
    # This query is too complex to be worth constructing in ORM, so just use raw SQL.
    cursor = connection.cursor()
    cursor.execute("""\
        SELECT t.time, t.device_id AS mac
        FROM (SELECT d.time, d.device_id, LAG(d.device_id) OVER(ORDER BY d.time) AS prev_device_id
            FROM (SELECT time, tankid, device_id
                FROM devices_datum
                WHERE tankid = %s
            ) AS d
        ) AS t WHERE t.device_id IS DISTINCT FROM t.prev_device_id;
    """, [tankid])

    history = dictfetchall(cursor)

    history_serializer = TankHistorySerializer(history, many=True)
    return JsonResponse(history_serializer.data, safe=False)

def dictfetchall(cursor):
    """
    Return all rows from a cursor as a dict
    """
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

@require_http_methods(["GET"])
def get_tank_sparklines(request, tankid):
    """
    Returns a response containing the history of the tanks's temp and pH over the last 24 hours.
    """
    # Sanitize tankid
    tankid = int(tankid)

    constraints = {
        'start': pytz.utc.localize(datetime.min),
        'end': timezone.now(),
        'freq': None,
        'cutoff': -10000,
        'total': 24
    }

    response = {
        'tankid': tankid,
        'sparklines': {
            'temp': [],
            'pH': []
        }
    }

    if request.GET.get('includeTime', default=False):
        response['sparklines']['time'] = []

    try:
        data = query_data(constraints, tankid=tankid)
    except ValueError:
        data = []
        response['error'] = "The specified tank does not have enough data to generate sparklines."

    for row in data:
        if request.GET.get('includeTime', default=False):
            response['sparklines']['time'].append(row['time'])
        response['sparklines']['temp'].append(row['temp'])
        response['sparklines']['pH'].append(row['pH'])

    sparkline_serializer = TankSparklineSerializer(response)

    return JsonResponse(sparkline_serializer.data, safe=False)
