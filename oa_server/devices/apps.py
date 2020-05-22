from django.apps import AppConfig


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
        except (psycopg2.OperationalError, django.db.utils.OperationalError):
            pass
