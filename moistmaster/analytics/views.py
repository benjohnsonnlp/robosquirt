import json

from django.views.generic import ListView

from .models import WateringSession


class WateringSessions(ListView):

    context_object_name = "sessions"
    model = WateringSession
    paginate_by = 15
    template_name = "watering_sessions.html"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.order_by("-session_start")

    def get_json_watering_data(self):
        data = self.model.objects.minutes_per_day(days=7)
        as_points = [{"x": d.date().isoformat(), "y":  s} for d, s in data]
        return json.dumps(as_points, indent=4)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if not context["page_obj"]:
            first_page = True
        else:
            first_page = context["page_obj"].number == 1
        context.update(
            data=self.get_json_watering_data(),
            first_page=first_page

        )
        return context