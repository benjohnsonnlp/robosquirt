import logging

from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from forecast.nws import ForecastEndpoint
from geo.forms import LocationLookupForm
from geo.load import GNISLoader
from geo.models import GeographicFeature, UserSettings


class Location(TemplateView):

    logger = logging.getLogger("moistmaster.geo")

    http_method_names = ["get", "post"]
    template_name = "location.html"
    mapbox_token = settings.MAPBOX_TOKEN

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        try:
            user_settings = UserSettings.objects.get()
            forecast = list(self.get_forecast(user_settings))[:6]
        except UserSettings.DoesNotExist:
            user_settings = None
            forecast = None
        context.update({
            "settings": user_settings,
            "mapbox_token": self.mapbox_token,
            "forecast_periods": forecast
        })
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        if "usgs_id" not in request.POST:
            raise ValueError("POST request missing a \"usgs_id\" value.")
        if not request.POST["usgs_id"].isdigit():
            raise ValueError("POST request's \"usgs_id\" value is not numeric but should be.")
        else:
            usgs_id = int(request.POST["usgs_id"])
            location = get_object_or_404(GeographicFeature, usgs_id=usgs_id)
            self.logger.info("Setting location to: {}".format(location))
            (user_settings, _) = UserSettings.objects.get_or_create()
            user_settings.set_location(location)
            return redirect("location")

    def get_forecast(self, user_settings):
        if user_settings.nws_hourly_endpoint:
            forecast = ForecastEndpoint(user_settings.nws_hourly_endpoint)
            return forecast.periods
        else:
            return []


class LocationLookup(TemplateView):

    form_class = LocationLookupForm
    logger = logging.getLogger("moistmaster.geo")
    http_method_names = ["get"]
    template_name = "location_lookup.html"

    @staticmethod
    def request_includes_lookup(request):
        return "state" in request.GET and "place" in request.GET

    @property
    def places_loaded(self):
        return GeographicFeature.objects.exists()

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if self.request_includes_lookup(request):
            form = self.form_class(request.GET)
            context.update({
                "form": form,
                "show_results": True,
                "results": self.lookup_places(form),
                "places_loaded": self.places_loaded
            })
        else:
            context.update({
                "form": LocationLookupForm(),
                "show_results": False,
                "results": None,
                "places_loaded": self.places_loaded
            })
        return self.render_to_response(context)

    def load_places_if_necessary(self):
        if self.places_loaded:
            return
        self.logger.info("No geographic features found in DB. Loading from bundled data...")
        loader = GNISLoader(settings.USGS_GNIS_DATA)
        loader.load()

    def lookup_places(self, form):
        if form.is_valid():
            state = form.cleaned_data["state"]
            place = form.cleaned_data["place"]
            self.load_places_if_necessary()
            results = [r for r in GeographicFeature.objects.filter(state=state, name__icontains=place)]
            return sorted(results, key=lambda r: (r.kind_priority, r.name))
        else:
            return None
