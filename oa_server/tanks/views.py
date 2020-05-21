from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, JsonResponse
from django.db import connection
from tanks.serializers import TankHistorySerializer
from devices.models import Device, Datum
from devices.views import get_constraints, query_data, create_csv

@require_http_methods(["GET"])
def get_tank_data(request, tankid):
    """
    Queries data from the specified tank ID according to constraints specified in the request.

    Returns the data as a CSV file.
    """
    # First, check if a device with the specified tank ID exists
    try:
        Device.objects.get(tankid=tankid)
    except Device.DoesNotExist:
        return HttpResponse("There is no device associated with the specified tank.", status=404)

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
