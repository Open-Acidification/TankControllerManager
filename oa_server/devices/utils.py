import platform
import subprocess
import re
import requests

def get_mac(address):
    mac = requests.get(f"http://{address}/mac", timeout=2)
    # Fail if API call yields wrong status code
    if mac.status_code != 200:
        raise ValueError(f"Received response code {mac.status_code}; expected 200")

    # Get everything before line break
    mac = mac.text.partition('\n')[0].strip().lower()
    # Fail if returned MAC is of invalid format
    if not re.match("[0-9a-f]{2}(:)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac):
        raise ValueError(f"The returned MAC address \"{mac}\" is invalid")

    return mac

def strip_mac(mac):
    """
    Simplifies the MAC address by removing all special characters.
    """
    return re.sub('[^a-f0-9]+', '', mac)

def ping(host):
    if host is None:
        return False

    # Chooses appropriate parameter depending on the platform
    param = '-n' if platform.system().lower() == 'windows' else '-c'

    command = ['ping', param, '1', host]

    return subprocess.call(command) == 0
