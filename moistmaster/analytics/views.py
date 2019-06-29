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