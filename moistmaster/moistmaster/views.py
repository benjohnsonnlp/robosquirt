from django.views.generic import RedirectView, TemplateView
from zmq import ZMQError

from analytics.models import WateringSession
from moistmaster.robosquirt import RobosquirtClient


client = RobosquirtClient()


class Index(TemplateView):

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        status = client.get_status()
        if status:
            valve_state = status["state"]
        else:
            valve_state = "unavailable"
        context.update({"valve_status": valve_state,
                        "valve_is_open": valve_state == "open",
                        "watering_sessions": WateringSession.objects.all().order_by("-session_start")})
        return context


class Toggle(RedirectView):

    http_method_names = ['post']
    pattern_name = "index"

    def post(self, request, *args, **kwargs):
        try:
            client.toggle()
        except ZMQError:
            pass
        return super().post(request, *args, **kwargs)
