import platform
import subprocess
from datetime import datetime
from contextlib import closing
import json
import csv
import pytz
import requests
from django.db import models

class Device(models.Model):
    name = models.CharField(max_length=64)
    ip = models.GenericIPAddressField(protocol='IPv4', unique=True)
    mac = models.CharField(max_length=17, primary_key=True)
    notes = models.TextField()
    last_refreshed = models.DateTimeField(auto_now=False, default=datetime.min)

    @property
    def online(self):
        return ping(self.ip)

    def refresh_data(self):
        if load_data(self, self.last_refreshed):
            self.last_refreshed = datetime.utcnow()
            return True
        return False

    # Automatically refresh data after saving
    # pylint: disable=W0222
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # TODO: Make this async using Celery
        self.refresh_data()

class Datum(models.Model):
    class Meta:
        unique_together = (('device', 'time'))
        verbose_name_plural = "Data"

    device = models.ForeignKey(Device, db_index=True, \
        on_delete=models.CASCADE) # Deleting a device deletes all its data
    time = models.DateTimeField(auto_now=False, db_index=True)
    tankid = models.IntegerField()
    temp = models.FloatField()
    temp_setpoint = models.FloatField()
    pH = models.FloatField()
    pH_setpoint = models.FloatField()
    on_time = models.IntegerField()
    Kp = models.FloatField()
    Ki = models.FloatField()
    Kd = models.FloatField()

def ping(host):
    if host is None:
        return False

    # Chooses appropriate parameter depending on the platform
    param = '-n' if platform.system().lower() == 'windows' else '-c'

    command = ['ping', param, '1', host]

    return subprocess.call(command) == 0

def load_csv(address, device):
    """
    Loads the CSV at the specified address and associates it with the specified device
    """
    imported_everything = True

    try:
        request = requests.get(address, stream=True, timeout=5)

        # Set up reader
        lines = (line.decode('utf-8') for line in request.iter_lines())
        reader = csv.reader(lines)

        # Skip header
        next(reader, None)
        # Import rows
        for row in reader:
            if len(row) == 10:
                Datum.objects.get_or_create(
                    device=device,
                    time=pytz.utc.localize(datetime.strptime(row[0], '%Y/%m/%d %H:%M:%S:%f')),
                    tankid=int(row[1]),
                    temp=float(row[2]),
                    temp_setpoint=float(row[3]),
                    pH=float(row[4]),
                    pH_setpoint=float(row[5]),
                    on_time=float(row[6]),
                    Kp=float(row[7]),
                    Ki=float(row[8]),
                    Kd=float(row[9])
                )
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
        imported_everything = False

    return imported_everything

def json_to_object(address):
    """
    Requests the JSON at the specified address and attempts to convert to object

    Returns the object if successful; None otherwise
    """
    try:
        request = requests.get(address, timeout=5)
        if request.status_code != 200:
            raise ValueError(f"Received response code {request.status_code}; expected 200")
        return json.loads(request.text)
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, \
        json.JSONDecodeError, ValueError):
        return None

# pylint: disable=R0912,R0914
# TODO: Refactor this to use recursion
def load_data(device, start_at=datetime.min):
    """
    Checks every file on the device for new data starting at the specified date

    Returns True if new data found and no errors are encountered; false otherwise
    """
    if not device.online:
        return False

    # Get the base URL for listing years
    base_url = f"http://{device.ip}/data"

    # Get list of years
    years = json_to_object(base_url)

    # We can't pull up the list of years, so fail
    if years is None:
        return False

    imported_everything = True

    for year in years:
        # Skip years that fall before our specified start time
        if int(year) < start_at.year:
            continue

        # Get the URL for listing months in the year
        year_url = f"{base_url}/{year}"

        # Get list of months
        months = json_to_object(year_url)

        # If this year is inaccessible, try the next
        if months is None:
            imported_everything = False
            continue

        for month in months:
            # Skip months that fall before our specified start time
            if int(year) == start_at.year & int(month) < start_at.month:
                continue

            # Get the URL for listing days in the month
            month_url = f"{year_url}/{month}"

            # Get list of days
            days = json_to_object(month_url)

            # If this month is inaccessible, try the next
            if days is None:
                imported_everything = False
                continue

            for day in days:
                # Skip days that fall before our specified start time
                if int(month) == start_at.month & int(day) < start_at.day:
                    continue

                # Get the URL for listing hours in the day
                day_url = f"{month_url}/{day}"

                # Get list of hours
                hours = json_to_object(day_url)

                # If this day is inaccessible, try the next
                if hours is None:
                    imported_everything = False
                    continue

                for hour in hours:
                    # Skip hours that fall before our specified start time
                    if int(day) == start_at.day & int(hour) < start_at.hour:
                        continue

                    # Get the URL for the hour's CSV
                    hour_url = f"{day_url}/{hour}"

                    # Load the CSV
                    imported_everything = imported_everything and load_csv(hour_url, device)
    return imported_everything

def reload_data(device):
    """Deletes and reloads data from the specified device"""
    Datum.objects.filter(device=device).delete()

    load_data(device)
