import platform
import subprocess
from datetime import datetime
from contextlib import closing
import json
import csv
import pytz
import requests
from django.db import models
from django_q.tasks import async_task, result, fetch
from django_q.models import Schedule

class Device(models.Model):
    name = models.CharField(max_length=32)
    ip = models.GenericIPAddressField(protocol='IPv4', unique=True)
    mac = models.CharField(max_length=17, primary_key=True)
    notes = models.TextField()
    download_task = models.CharField(max_length=32, default="")
    schedule = models.ForeignKey(Schedule, blank=True, null=True, \
        on_delete=models.CASCADE)
    last_refreshed = models.DateTimeField(auto_now=False, default=datetime.min)

    @property
    def online(self):
        return ping(self.ip)

    def scheduled_refresh(self):
        """
        The method to be called for a scheduled refresh.

        Schedule creates its own asynchronous task, so load_data() is called synchronously here.
        """
        # First make sure that the device has a schedule associated with it
        if self.schedule is None:
            return False
        # If the lock didn't get released but the task is finished, ignore it
        if self.download_task == "" or result(self.download_task) is not None:
            self.download_task = self.schedule.task
            result = self.load_data(start_at=self.last_refreshed)
            self.finish_download(fetch(self.download_task))

    def refresh_data(self, start_at=None, reload_data=False):
        """
        Asynchronous wrapper method for load_data()
        """
        if start_at is None:
            # We can't use self for default argument
            start_at = self.last_refreshed
        # If the lock didn't get released but the task is finished, ignore it
        if self.download_task == "" or result(self.download_task) is not None:
            self.download_task = async_task(self.load_data, hook=self.finish_download, \
                start_at=start_at, reload_data=reload_data)

    # pylint: disable=R0912,R0914
    # TODO: Refactor this to use recursion
    def load_data(self, start_at=datetime.min, reload_data=False):
        """
        Checks every file on the device for new data starting at the specified date.
        If reload is True, deletes existing data before reloading

        Returns True if new data found and no errors are encountered; false otherwise
        """
        # For the sake of clarity
        device = self

        if not device.online:
            return False

        if reload_data:
            Datum.objects.filter(device=device).delete()

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

    def finish_download(self, task):
        # Release the lock
        self.download_task = ""

        # If all went well, update the last refreshed time
        if task.result:
            self.last_refreshed = datetime.utcnow()

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
