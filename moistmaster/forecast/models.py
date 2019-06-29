from django.db import models


from .managers import ForecastQuerySet


class Forecast(models.Model):

    period_index = models.IntegerField(primary_key=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    is_daytime = models.BooleanField()
    temperature = models.IntegerField()
    forecast_short = models.TextField()
    forecast_long = models.TextField()
    precipitation_probability = models.TextField()
    is_daytime = models.BooleanField()
    icon_type = models.TextField()

    objects = ForecastQuerySet.as_manager()

    def __str__(self):
        return "Forecast {}".format(self.period_index)

    def __repr__(self):
        return "<Forecast {}>".format(self.period_index)

