from django.conf import settings
from django.conf.urls import url
from django.urls import include, path
from django.views import defaults as default_views
import debug_toolbar

from .views import Login, Index, ResetPassword, SetPassword, Toggle
from geo.views import Location, LocationLookup

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("login", Login.as_view(), name="login"),
    path("set-password", SetPassword.as_view(), name="set-password"),
    path("reset-password", ResetPassword.as_view(), name="reset-password"),
    path("toggle/", Toggle.as_view(), name="toggle"),
    path("location/", Location.as_view(), name="location"),
    path("location/lookup", LocationLookup.as_view(), name="location-lookup")
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
        url(r'^__debug__/', include(debug_toolbar.urls))]
