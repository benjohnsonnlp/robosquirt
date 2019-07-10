import ciso8601
import logging
from django.db import models

from forecast.nws import ForecastEndpoint
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

    def reload_nws_forecasts(self):
        user_settings = UserSettings.objects.get()
        forecast_endpoint = ForecastEndpoint(user_settings.nws_hourly_endpoint)
        removed_count = self.all().count()
        self.all().delete()
        forecast_periods = []
        for period in forecast_endpoint.periods:
            self.create(period_index=period["number"],
                        start=ciso8601.parse_datetime(period["startTime"]),
                        end=ciso8601.parse_datetime(period["endTime"]),
                        is_daytime=period["isDaytime"],
                        temperature=period["temperature"],
                        forecast_short=period["shortForecast"],
                        forecast_long=period["detailedForecast"],
                        precipitation_probability=period["precipitationProbability"],
                        icon_type=period["iconType"])
        added_count = len(forecast_periods)
        self.logger.info("Removed {} existing forecasts and saved {} new forecasts.".format(removed_count, added_count))
