import ciso8601
import collections
from datetime import datetime, timedelta
from dateutil.tz import tzlocal
import functools
import itertools
import logging
from noaa_sdk import noaa
import spacy



logging.getLogger("robosquirt.forecasts")

nlp = spacy.load('en_core_web_sm')


RAIN = 1
STORM = 2
CLOUDS = 3
SUN = 4


@functools.total_ordering
class Forecast:

    def __init__(self, start, end, is_day, temp, wind, forecast, icon):
        self.start = start
        self.end = end
        self.is_day = is_day
        self.temp = temp
        self.wind = wind
        self.forecast = forecast
        self.icon = icon

    @classmethod
    def from_api_response(cls, resp):
        return cls(start=ciso8601.parse_datetime(resp["startTime"]),
                   end=ciso8601.parse_datetime(resp["endTime"]),
                   is_day=resp["isDaytime"],
                   temp=(resp["temperature"], resp["temperatureUnit"]),
                   wind=(resp["windSpeed"], resp["windDirection"]),
                   forecast=resp["shortForecast"],
                   icon=resp["icon"]
                   )

    def __eq__(self, other):
        return self.start == other.start

    def __lt__(self, other):
        return self.start < other.start

    def __repr__(self):
        return "<Forecast {} - {}>".format(self.start.isoformat(), self.end.isoformat())

    def parsed_forecast(self):
        doc = nlp(self.forecast)
        return doc



class ForecastRange(collections.UserList):

    def __init__(self, forecasts):
        super(ForecastRange, self).__init__(forecasts)

    def __repr__(self):
        return "<ForecastRange {} - {}>".format(self.data[0].start.isoformat(),
                                                self.data[-1].end.isoformat())

    def __getitem__(self, item):
        if isinstance(item, int):
            return super(ForecastRange, self).__getitem__(item)
        if isinstance(item, datetime):
            for forecast in self:
                if forecast.start == item:
                    return forecast
            raise IndexError("Date {} not found in range.")
        if isinstance(item, slice):
            if isinstance(item.start, datetime) and isinstance(item.stop, datetime):
                return ForecastRange([f for f in self if f.start >= item.start and f.end <= item.stop])
            return ForecastRange(super(ForecastRange, self).__getitem__(item))

    @staticmethod
    def now():
        return datetime.now(tzlocal())

    @classmethod
    def from_zipcode(cls, zipcode):
        n = noaa.NOAA()
        try:
            all_results = n.get_forecasts(zipcode, 'US', True)
        except ConnectionError as exc:
            logging.warning("Could not fetch forecast data: {}".format(exc))
            return cls([])
        return cls(sorted([Forecast.from_api_response(r) for r in all_results]))

    def group_by_property(self, property):
        grouped_forecasts = itertools.groupby(self, key=lambda fc: getattr(fc, property))
        for val, group in grouped_forecasts:
            group = list(group)
            yield (group[0].start, group[-1].end, val)

    def print_grouped_property(self, property):
        date_fmt = "%b %d, %Y"
        time_fmt = "%I:%M %p"

        for start, end, value in self.group_by_property(property):
            if start.date() == end.date():
                print("{} {} - {}: {}".format(start.strftime(date_fmt),
                                              start.strftime(time_fmt),
                                              end.strftime(time_fmt),
                                              value))
            else:
                print("{} {} - {} {}: {}".format(start.strftime(date_fmt),
                                                 start.strftime(time_fmt),
                                                 end.strftime(date_fmt),
                                                 end.strftime(time_fmt),
                                                 value))

    def slice_from_now(self, hours=12):
        start = self.now()
        end = start + timedelta(hours=hours)
        return self[start:end]
