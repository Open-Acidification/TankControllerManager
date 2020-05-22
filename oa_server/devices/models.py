from datetime import datetime
from contextlib import closing
import json
import csv
import pytz
import requests
from django.db import models, utils
from django_q.tasks import async_task, result, fetch
from django_q.models import Task, Schedule
from devices.utils import get_mac

class Device(models.Model):
    name = models.CharField(max_length=32)
    ip = models.GenericIPAddressField(protocol='IPv4', unique=True)
    mac = models.CharField(max_length=17, primary_key=True)
    notes = models.TextField()
    downloading = models.BooleanField(default=False)
    schedule = models.ForeignKey(Schedule, blank=True, null=True, \
        on_delete=models.CASCADE)
    next_path = models.CharField(max_length=16, default="")

    @property
    def status(self):
        return verify_mac(self.mac, self.ip)


    def scheduled_refresh(self):
        """
        The method to be called for a scheduled refresh.

        Schedule creates its own asynchronous task, so lock_and_load() is called synchronously here.
        """
        # First make sure that the device has a schedule associated with it
        if self.schedule is None:
            return ["This device has no associated schedule."]
        if not self.downloading:
            task_id = Task.objects.latest('started').id

            load_result = self.lock_and_load()
            self.finish_download(fetch(task_id))
            return load_result
        return "The device is already downloading."

    def refresh_data(self, reload_data=False):
        """
        Asynchronous wrapper method for lock_and_load()
        """
        if not self.downloading:
            async_task(self.lock_and_load, hook=self.finish_download, reload_data=reload_data)


    def lock(self):
        "Acquire a lock for downloading."
        self.downloading = True
        self.save()

    def unlock(self):
        "Release the download lock."
        self.downloading = False
        self.save()


    def lock_and_load(self, start_path=None, reload_data=False):
        """
        Wrapper method for load_data()
        Acquires a lock and releases it in the event of an unhandled exception.
        """
        try:
            # Acquire the lock
            self.lock()

            # Attempt to download
            return load_data(self, start_path, reload_data)

        except:
            # Release the lock
            self.unlock()

            # Re-raise the exception, like the responsible programmers we are
            raise

    def finish_download(self, task):
        # Release the lock
        self.downloading = False

        # Update the next path
        self.next_path = task.result[0]
        self.save()

def verify_mac(mac, address):
    """
    Verifies that the supplied MAC address matches that of the supplied IP address

    Return values:
    0 = Device is offline
    1 = MAC address in DB matches MAC address returned by device
    2 = MAC address in DB does not match MAC address returned by device
    """
    try:
        status = mac == get_mac(address)
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, ValueError):
        return 0

    if status:
        return 1

    return 2

def load_data(device, start_path=None, reload_data=False):
    """
    Checks every file on the device for new data starting at the specified date.
    If reload is True, deletes existing data before reloading

    Returns a list of inaccessible endpoints, or a list containing the single last endpoint
    """
    # We can't use self for default argument
    if start_path is None:
        start_path = device.next_path

    if device.status == 0:
        # We return the start_path as the first element
        # so that it remains as such during cleanup.
        return [start_path, "Error: The device is offline."]
    if device.status == 2:
        return [start_path, "Error: The device address has changed. Update IP address."]

    # Delete all existing data if a full reload is requested
    if reload_data:
        Datum.objects.filter(device=device).delete()

    # Get the base URL from the device's IP
    base_url = f"http://{device.ip}/data"

    # Ensure that our starting point has four values, even if the provided path is incomplete
    start_at = [0, 0, 0, 0]

    # Update starting point to match path
    endpoints = start_path.split('/')
    for idx in range(min(len(endpoints), 4)):
        # Only accept valid integers for endpoints
        try:
            endpoint = int(endpoints[idx])
        except (ValueError, TypeError):
            endpoint = 0
        start_at[idx] += endpoint

    # We will fill this array with any paths for which we fail to download data
    missed_paths = []

    # Begin recursion
    last_path = load_data_recursive(device, start_at, base_url, missed_paths)

    # If we didn't miss any paths, the last path becomes the next one with which to start
    if not missed_paths:
        missed_paths.append(last_path)

    return missed_paths

def load_csv(address, device):
    """
    Loads the CSV at the specified address and associates it with the specified device

    Returns: 0 for error, 1 for success, and 2 for end of file
    """

    try:
        request = requests.get(address, stream=True, timeout=5)

        # If HTTP status code is 416, we've reached the end of the file
        if request.status_code == 416:
            return 2

        # Set up reader
        lines = (line.decode('utf-8') for line in request.iter_lines())
        reader = csv.reader(lines)

        # Skip header
        next(reader, None)

        # Import rows
        for row in reader:
            # Ignore lines of improper length
            if len(row) == 7:
                try:
                    Datum.objects.create(
                        device=device,
                        time=pytz.utc.localize(datetime.strptime(row[0], '%Y/%m/%d %H:%M:%S')),
                        tankid=int(row[1]),
                        temp=float(row[2]),
                        temp_setpoint=float(row[3]),
                        pH=float(row[4]),
                        pH_setpoint=float(row[5]),
                        on_time=int(row[6])
                    )
                # Ignore lines if they aren't formatted correctly or already exist
                except (utils.IntegrityError, ValueError):
                    pass

    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, \
        requests.exceptions.ChunkedEncodingError, UnicodeDecodeError):
        return 0

    return 1

def page_csv(address, device):
    """
    Repeatedly call load_csv() in 100-line pages until the end is reached

    Return True if successful; False if error encountered
    """
    line = 0

    status = 1

    while status == 1:
        status = load_csv(f"{address}?start={line}&num=100", device)
        line += 100

    return bool(status)

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

# Pylint requires five or fewer arguments in order to encourage refactoring,
# but that's not really relevant here.
#pylint: disable=too-many-arguments
def load_data_recursive(device, start_at, base_url, missed_paths, path='', level=0):
    """
    Recursive helper function for load_data()
    """
    if level < 4:
        # We need to go deeper
        directories = json_to_object(base_url + path)

        # If this endpoint returns no directories, add it as a missed path
        if directories is None:
            missed_paths.append(path)
            return path

        # Define the last path visited by this branch
        last_path = ''
        for directory in directories:
            # Skip directories that come before our starting point
            if int(directory) < start_at[level]:
                continue
            # Call the function for this subdirectory
            last_path = load_data_recursive(device, start_at, base_url, \
                missed_paths, path+'/'+directory, level+1)
        return last_path

    # We've reached a CSV
    load_success = page_csv(base_url + path, device)

    if not load_success:
        missed_paths.append(path)

    return path

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
