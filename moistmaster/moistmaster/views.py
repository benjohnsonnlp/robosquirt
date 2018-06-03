from django.views.generic import RedirectView, TemplateView

from moistmaster.robosquirt import RoboSquirtProxy


proxy = RoboSquirtProxy()


class Index(TemplateView):

    template_name = "index.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({"valve_status": proxy.status,
                        "valve_is_open": proxy.is_open},)
        return context


class Toggle(RedirectView):

    http_method_names = ['post']
    pattern_name = "index"


    def post(self, request, *args, **kwargs):
        proxy.toggle()
        return super().post(request, *args, **kwargs)
