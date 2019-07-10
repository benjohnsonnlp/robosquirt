"""
National Weather Service API
"""
import logging
import requests


class BaseEndpoint:
    logger = logging.getLogger("robosquirt")

    headers = {
        'User-Agent': 'Moistmaster: Automated Watering Controller (v1.0)'
    }

    def get_json(self, url):
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()


class PointEndpoint(BaseEndpoint):
    url = "https://api.weather.gov/points/{},{}"

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        self.properties = self.get_properties()

    def get_properties(self):
        url = self.url.format(round(self.latitude, 4), round(self.longitude, 4))
        self.logger.info("Querying National Weather Service location endpoint: {}".format(url))
        response = self.get_json(url)
        return response["properties"]

    @property
    def forecast_url(self):
        return self.properties["forecast"]

    @property
    def hourly_forecast_url(self):
        return self.properties["forecastHourly"]


class ForecastEndpoint(BaseEndpoint):

    def __init__(self, url):
        self.logger.info("Querying National Weather Service forecast endpoint: {}".format(url))
        response = self.get_json(url)
        self.properties = response["properties"]

    @property
    def periods(self):
        for period in self.properties["periods"]:
            forecast = ForecastParser(period)
            period.update({
                "precipitationProbability": forecast.precipitation_probability,
                "isDaytime": forecast.is_daytime,
                "iconType": forecast.icon_type
            })
            yield period


class ForecastParser:

    precipitation_not_expected = (
        "partly cloudy",
        "partly sunny",
        "mostly sunny",
        "mostly clear",
        "mostly cloudy",
        "sunny",
        "clear"
    )

    low_probability = ("LOW", (
        "slight chance rain showers",
        "slight chance showers",
        "slight chance thunderstorms",
        "slight chance showers and thunderstorms"
        "isolated showers",
        "isolated showers and thunderstorms",

    ))
    medium_probability = ("MODERATE", (
        "chance rain showers",
        "chance showers",
        "chance thunderstorms",
        "scattered showers",
    ))
    high_probability = ("HIGH", (
        "rain likely"
        "showers likely",
        "showers and thunderstorms likely",
        "showers and thunderstorms",
    ))

    def __init__(self, period):
        self.normalized_short_forecast = period["shortForecast"].lower().strip()
        self.is_daytime = "/icons/land/day/" in period["icon"]

    @property
    def precipitation_probability(self):
        for forecast in self.precipitation_not_expected:
            if forecast == self.normalized_short_forecast:
                return "NONE"
        for (prob, fragments) in [self.low_probability, self.medium_probability, self.high_probability]:
            for fragment in fragments:
                if fragment in self.normalized_short_forecast:
                    return prob
        return "UNKNOWN"

    @property
    def icon_type(self):
        if self.precipitation_probability in {"HIGH", "MODERATE"}:
            if "thunderstorm" in self.normalized_short_forecast:
                return "TSTORM"
            else:
                return "RAIN"
        for descriptor in ("clear", "sunny", "mostly clear", "mostly sunny"):
            if descriptor in self.normalized_short_forecast:
                if self.is_daytime:
                    return "SUN"
                else:
                    return "MOON"
        return "CLOUD"
