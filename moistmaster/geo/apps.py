import logging

from django.apps import AppConfig


class GeoConfig(AppConfig):

    logger = logging.getLogger("moistmaster")
    name = 'geo'
