from django.contrib.postgres.fields import ArrayField
from django.db import models

class TimeSeries(models.Model):
    TS_TYPES = [
        ('P', 'pH'),
        ('T', 'Temperature'),
    ]
    name = models.CharField(max_length=64)
    value = ArrayField(models.FloatField())
    time = ArrayField(models.PositiveIntegerField())
    interval = models.PositiveIntegerField(default=0)
    notes = models.TextField()
    type = models.CharField(max_length=1, choices=TS_TYPES)
