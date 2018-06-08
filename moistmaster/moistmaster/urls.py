from django.conf import settings
from django.conf.urls import url
from django.urls import include, path
from django.views import defaults as default_views
import debug_toolbar

from .views import Index, Toggle

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("toggle/", Toggle.as_view(), name="toggle")
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
