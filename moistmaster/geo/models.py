from django.db import models

from forecast.nws import PointEndpoint
from geo.managers import UserSettingsQuerySet


class GeographicFeature(models.Model):

    usgs_id = models.IntegerField(primary_key=True)
    name = models.TextField(null=False)
    kind = models.TextField(null=False)
    state = models.CharField(max_length=2, null=False, db_index=True)
    county = models.TextField(null=False)
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)
    elevation = models.IntegerField(null=True)

    def __str__(self): return "{}, {}".format(self.name, self.state)

    @property
    def kind_priority(self):
        normalized_kind = self.kind.upper()
        if normalized_kind == "CIVIL":
            return 1
        elif normalized_kind == "POPULATED PLACE":
            return 2
        elif normalized_kind == "AIRPORT":
            return 3
        elif normalized_kind == "ISLAND":
            return 4
        elif normalized_kind == "CENSUS":
            return 5
        elif normalized_kind == "MILITARY":
            return 6
        else:
            return 7


class UserSettings(models.Model):

    location = models.ForeignKey(GeographicFeature, on_delete=models.SET_NULL, null=True)
    email = models.EmailField(blank=True)
    nws_daily_endpoint = models.URLField(blank=True)
    nws_hourly_endpoint = models.URLField(blank=True)

    objects = UserSettingsQuerySet.as_manager()

    def set_location(self, geographic_feature):
        self.location = geographic_feature
        point = PointEndpoint(geographic_feature.latitude, geographic_feature.longitude)
        self.nws_daily_endpoint = point.forecast_url
        self.nws_hourly_endpoint = point.hourly_forecast_url
        self.save()
