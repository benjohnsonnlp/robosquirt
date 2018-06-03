from django.views.generic import RedirectView, TemplateView

from moistmaster.robosquirt import RobosquirtClient


client = RobosquirtClient()


class Index(TemplateView):

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        valve_state = client.get_status()["state"]
        context.update({"valve_status": valve_state,
                        "valve_is_open": valve_state == "open"},)
        return context


class Toggle(RedirectView):

    http_method_names = ['post']
    pattern_name = "index"

    def post(self, request, *args, **kwargs):
        client.toggle()
        return super().post(request, *args, **kwargs)
