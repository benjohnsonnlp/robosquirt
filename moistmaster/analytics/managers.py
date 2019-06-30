import logging
from datetime import timedelta
from itertools import groupby

from django.db import models
from django.db.models.functions import TruncDay

from moistmaster.utils import utc_now


class WateringSessionQuerySet(models.QuerySet):
    logger = logging.getLogger("moistmaster")

    def gallons_used(self, days=25):
        start_from = utc_now() - timedelta(days=days)
        return sum(session.gallons for session in self.filter(session_start__gte=start_from))

    def minutes_per_day(self, days=25):
        now = utc_now().replace(hour=0, minute=0, second=0, microsecond=0)
        start_from = now - timedelta(days=days)
        records = (self
                   .filter(session_start__gte=start_from)
                   .order_by("session_start")
                   .annotate(day=TruncDay("session_start")))
        days_with_water = {}
        for (day, sessions) in groupby(records, key=lambda s: s.day):
            total_seconds = sum(s.length for s in sessions)
            days_with_water[day] = total_seconds
        daily_totals = []
        for delta_days in range(0, days + 1):
            day = now - timedelta(days=delta_days)
            daily_totals.append((day, days_with_water.get(day, 0)))
        return daily_totals
