import logging

from django.apps import AppConfig


class GeoConfig(AppConfig):

    logger = logging.getLogger("moistmaster")
    name = 'geo'

    def ready(self):
        from .models import UserSettings
        UserSettings.objects.get_or_create_default()
