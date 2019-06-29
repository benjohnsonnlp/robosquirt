import logging
from datetime import timedelta
from django.db import models

from moistmaster.utils import utc_now


class WateringSessionQuerySet(models.QuerySet):

    logger = logging.getLogger("moistmaster")

    def gallons_used(self, days=25):
        start_from = utc_now() - timedelta(days=days)
        return sum(session.gallons for session in self.filter(session_start__gte=start_from))
