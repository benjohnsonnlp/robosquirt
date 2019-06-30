import ciso8601
import logging
from django.db import models

from geo.models import UserSettings
from moistmaster.utils import utc_now


class ForecastQuerySet(models.QuerySet):

    logger = logging.getLogger("moistmaster")

    def current_forecast(self, retry=1):
        result = self.order_by("start").filter(end__gte=utc_now())
        if result.exists():
            return result[0]
        else:
            if retry > 0:
                self.reload_nws_forecasts()
                self.current_forecast(retry=retry - 1)

    def future_forecasts(self):
        return self.order_by("start").filter(start__gte=utc_now())

    def past_forecasts(self):
        return self.order_by("start").filter(end__lte=utc_now())
