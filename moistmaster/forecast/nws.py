"""
National Weather Service API
"""
import logging

import requests


class BaseEndpoint:

    logger = logging.getLogger("moistmaster")

    headers = {
        'User-Agent': 'Moistmaster: Automated Watering Controller (v1.0)'
    }

    def get_json(self, url):
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()


class Point(BaseEndpoint):

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
        return self.properties["forecast"]



class Forecast(BaseEndpoint):

    def __init__(self, url):
        self.logger.info("Querying National Weather Service forecast endpoint: {}".format(url))
        response = self.get_json(url)
        self.properties = response["properties"]

    @property
    def periods(self):
        return self.properties["periods"]

