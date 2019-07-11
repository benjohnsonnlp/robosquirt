from django.conf import settings
from django.contrib.auth.forms import SetPasswordForm, AuthenticationForm, UsernameField
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django import forms
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import RedirectView, TemplateView, FormView
from zmq import ZMQError

from analytics.models import WateringSession
from forecast.models import Forecast
from geo.models import UserSettings
from robosquirt.client import RobosquirtClient


client = RobosquirtClient()


class LoginOrPasswordSetRequired(LoginRequiredMixin):

    def password_must_be_set(self):
        try:
            user = User.objects.get()
        except User.DoesNotExist:
            return True
        else:
            return not user.has_usable_password()

    def handle_no_permission(self):
        if self.password_must_be_set():
            return redirect("set-password")
        return super().handle_no_permission()


class Index(LoginOrPasswordSetRequired, TemplateView):

    template_name = "index.html"

    def forecast_icon_and_label(self, forecast):
        if not forecast:
            return "", "unknown"
        if forecast.icon_type == "SUN":
            return "images/svg-icons/sun.svg", "Clear skies"
        if forecast.icon_type == "MOON":
            return "images/svg-icons/moon.svg", "Clear skies"
        if forecast.icon_type == "RAIN":
            return "images/svg-icons/rain.svg", "Rain"
        if forecast.icon_type == "TSTORM":
            return "images/svg-icons/thunderstorm.svg", "Stormy"
        return "images/svg-icons/cloud.svg", "Cloudy"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        status = client.get_status()
        user_settings = UserSettings.objects.get_or_create_default()
        forecast = Forecast.objects.current_forecast()
        forecast_icon, forecast_label = self.forecast_icon_and_label(forecast)
        if status:
            valve_state = status["state"]
        else:
            valve_state = "unavailable"
        context.update({"gallons_used": WateringSession.objects.gallons_used(),
                        "user_settings": user_settings,
                        "forecast": forecast,
                        "forecast_icon": forecast_icon,
                        "forecast_label": forecast_label,
                        "valve_status": valve_state,
                        "valve_is_open": valve_state == "open",
                        "watering_sessions": WateringSession.objects.all().order_by("-session_start")})
        return context


class Toggle(LoginOrPasswordSetRequired, RedirectView):

    http_method_names = ['post']
    pattern_name = "index"

    def post(self, request, *args, **kwargs):
        try:
            client.toggle()
        except ZMQError:
            pass
        return super().post(request, *args, **kwargs)


class SetPassword(FormView):

    form_class = SetPasswordForm
    success_url = reverse_lazy('index')
    template_name = "set_password.html"

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated and self.request.user.has_usable_password:
            return HttpResponseForbidden("Password already set.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.get_or_create_user()
        return kwargs

    def get_or_create_user(self):
        try:
            user = User.objects.get()
        except User.DoesNotExist:
            user = User.objects.create_user(settings.DEFAULT_USERNAME,
                                            '{}@example.com'.format(settings.DEFAULT_USERNAME))
            UserSettings.objects.create(email='{}@example.com'.format(settings.DEFAULT_USERNAME))
        return user


class ResetPassword(LoginRequiredMixin, View):

    http_method_names = ["post"]
    raise_exception = True

    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get()
        except User.DoesNotExist:
            return
        user.set_unusable_password()
        user.save()
        return redirect(reverse("set-password"))


class Login(LoginView):

    class SimpleAuthenticationForm(AuthenticationForm):
        username = UsernameField(
            max_length=5,
            widget=forms.HiddenInput(),
        )
        password = forms.CharField(
            label="Password",
            strip=False,
            widget=forms.PasswordInput(attrs={'autofocus': True})
        )

    form_class = SimpleAuthenticationForm
    template_name = "login.html"

    def dispatch(self, request, *args, **kwargs):
        return super(Login, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {"username": settings.DEFAULT_USERNAME}
        return kwargs
