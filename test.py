import subprocess

out = subprocess.call('ping', '-c', '1', 'google.com')
print(out)