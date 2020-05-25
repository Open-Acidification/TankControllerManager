from django.apps import AppConfig
import psycopg2
import django.db.utils

class DevicesConfig(AppConfig):
    name = 'devices'

    def ready(self):
        # Pylint warns against this, but this is necessary as it
        # prevents an AppRegistryNotReady error.
        #pylint: disable=import-outside-toplevel
        from .models import Device

        try:
            # The Django docs recommend against interacting with the database here,
            # but this is the only way to ensure that all locks are released.
            for device in Device.objects.all():
                device.unlock()
        except (psycopg2.OperationalError, django.db.utils.OperationalError, \
            django.db.utils.ProgrammingError):
            # The devices table hasn't been created yet
            pass
