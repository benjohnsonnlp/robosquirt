from django.conf import settings
from django.db import models
import logging


class UserSettingsQuerySet(models.QuerySet):

    logger = logging.getLogger("moistmaster")

    def get_or_create_default(self):
        try:
            return self.get()
        except self.model.DoesNotExist:
            self.create(email='{}@example.com'.format(settings.DEFAULT_USERNAME))
            logging.info("No user settings found, created default record.")
            return self.get()
