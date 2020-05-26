from datetime import datetime
from contextlib import closing
import json
import csv
import pytz
import requests
from django.db import models, utils
from django.contrib.postgres.fields import ArrayField
from django_q.tasks import async_task, fetch
from django_q.models import Task, Schedule
from devices.utils import get_mac

class Device(models.Model):
    name = models.CharField(max_length=32)
    ip = models.GenericIPAddressField(protocol='IPv4')
    mac = models.CharField(max_length=17, primary_key=True)
    notes = models.TextField()
    downloading = models.BooleanField(default=False)
    schedule = models.ForeignKey(Schedule, blank=True, null=True, \
        on_delete=models.CASCADE)
    next_path = models.CharField(max_length=27, default="")
    missed_paths = ArrayField(models.CharField(max_length=27), default=list)

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
            load_result = self.lock_and_load()
            return load_result
        return "The device is already downloading."

    def refresh_data(self, reload_data=False):
        """
        Asynchronous wrapper method for lock_and_load()
        """
        if not self.downloading:
            async_task(self.lock_and_load, reload_data=reload_data)


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
            result = load_data(self, start_path, reload_data)

            # Clean up after downloading and return the result
            self.finish_download(result)
            return result
        except:
            # Release the lock
            self.unlock()

            # Re-raise the exception, like the responsible programmers we are
            raise

    def finish_download(self, result):
        # Release the lock
        self.downloading = False

        # Update the next path
        if result['next']:
            self.next_path = result['next']
        self.missed_paths = result['missed']
        self.save()

    def retry_paths(self):
        # Fill this with the paths that still fail upon retry
        missed_paths = []

        # Revisit each path
        for raw_path in self.missed_paths:
            path = path_as_list(raw_path)

            level = path['depth']
            path = path['path']

            base_url = f"http://{self.ip}/data"

            # We need to recursively visit all subpaths.
            # If any failures are encountered, they will be added to missed_paths
            if level < 4:
                load_data_recursive(self, path, base_url, missed_paths, level=level)

            # We're already at a CSV path
            else:
                address = f"{base_url}/{path[0]}/{path[1]}/{path[2]}/{path[3]}?start=" \
                    + str(int(path[4])*100) + "&num=100"
                status = load_csv(address, self)

                if not status:
                    # If this path still fails to download, re-add it to the missed paths
                    missed_paths.append(raw_path)

        # Save and return the paths we're still missing
        self.missed_paths = missed_paths
        self.save()

        return missed_paths

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
        # We return an error message while changing nothing on the device.
        return {'error': "The device is offline.", \
            'missed': device.missed_paths, 'next': device.next_path}
    if device.status == 2:
        return {'error': "The device address has changed. Update IP address.", \
            'missed': device.missed_paths, 'next': device.next_path}

    # Delete all existing data if a full reload is requested
    if reload_data:
        Datum.objects.filter(device=device).delete()

    # Get the base URL from the device's IP
    base_url = f"http://{device.ip}/data"

    # Ensure that our starting point has five values, even if the provided path is incomplete
    start_at = path_as_list(start_path)['path']
    print(start_at)

    # We will fill this array with any paths for which we fail to download data
    new_missed_paths = []

    # Begin recursion
    last_path = load_data_recursive(device, start_at, base_url, new_missed_paths)

    missed_paths = device.retry_paths()
    missed_paths.extend(new_missed_paths)

    return {'missed': missed_paths, 'next': last_path}

# Pylint requires five or fewer arguments in order to encourage refactoring,
# but that's not really relevant here.
#pylint: disable=too-many-arguments
def load_data_recursive(device, start_at, base_url, missed_paths, path='', level=0):
    """
    Recursive helper function for load_data()
    """
    print("Level: "+str(level)+", path: "+path)
    if level < 4:
        # We need to go deeper
        directories = json_to_object(base_url + path)

        # If this endpoint cannot be accessed, add it as a missed path
        if directories is None:
            missed_paths.append(path)
            return path

        # Define the last path visited by this branch
        last_path = device.next_path
        for directory in directories:
            # Skip directories that come before our starting point
            if int(directory) < start_at[level]:
                continue

            # Now that we've skipped all endpoints up to our start point at this level,
            # stop skipping for future iterations
            start_at[level] = 0

            # Call the function for this subdirectory
            last_path = load_data_recursive(device, start_at, base_url, \
                missed_paths, path+'/'+directory, level+1)

        return last_path

    # We've reached a CSV
    load_result = page_csv(base_url + path, device, start_at[4])

    if not load_result['success']:
        missed_paths.append(path+'/'+str(load_result['end_page']))

    # Make sure that we start at the first page for all subsequent endpoints
    start_at[4] = 0

    return path

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

def page_csv(address, device, page=0):
    """
    Repeatedly call load_csv() in 100-line pages until the end is reached

    Return True if successful; False if error encountered
    """
    status = 1

    line = page * 100

    while status == 1:
        status = load_csv(f"{address}?start={line}&num=100", device)
        line += 100

    page = (line // 100) - 1

    return {'success': bool(status), 'end_page': page}

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

def path_as_list(path):
    """
    Converts a path in the form of /year/month/day/hour/page to a list containing those elements.
    """
    path_list = [0, 0, 0, 0, 0]

    # Split the given path into an array
    endpoints = path.split('/')
    depth = len(endpoints)
    # Ensure that this array is of the proper length by combining it with path_list
    for idx in range(min(depth, 5)):
        # Only accept valid integers for endpoints
        try:
            endpoint = int(endpoints[idx])
        except (ValueError, TypeError):
            endpoint = 0
        path_list[idx] += endpoint

    return {'path': path_list, 'depth': depth}

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
