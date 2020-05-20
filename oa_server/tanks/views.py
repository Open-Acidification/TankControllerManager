from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from devices.models import Device
from devices.views import get_constraints, query_data, create_csv

@require_http_methods(["GET"])
def get_tank_data(request, tankid):
    """
    Queries data from the specified tank ID according to constraints specified in the request.

    Returns the data as a CSV file.
    """
    # First, check if a device with the specified tank ID exists
    try:
        device = Device.objects.get(tankid=tankid)
    except Device.DoesNotExist:
        return HttpResponse("There is no device associated with the specified tank.", status=404)

    constraints = get_constraints(request)

    data = query_data(constraints, tankid=tankid)

    download = bool(request.GET.get('download', default=False))
    show_device = bool(request.GET.get('showDevice', default=False))

    return create_csv(data, download, 'tankid-'+tankid, show_device)
