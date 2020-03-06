from django.db import models

class Device(models.Model):
    name = models.CharField(max_length=64)
    ip = models.GenericIPAddressField(protocol='IPv4', unique=True)
    mac = models.CharField(max_length=12, primary_key=True)
    notes = models.TextField()