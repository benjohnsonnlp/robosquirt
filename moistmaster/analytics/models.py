from django.db import models
from django.utils.timezone import now
import math

from .managers import WateringSessionQuerySet

#: FIXME: This should not be a constant.
GALLONS_PER_MINUTE = 2.1


class WateringSession(models.Model):
    """
    A DB representation of a watering session (i.e a period of time when a valve was turned on then off).
    """
    identifier = models.CharField(max_length=36, primary_key=True)
    created_time = models.DateTimeField(null=False)
    session_start = models.DateTimeField(null=False)
    session_end = models.DateTimeField()
    device_identifier = models.IntegerField(null=False)
    originator = models.TextField()
    reason = models.TextField()

    objects = WateringSessionQuerySet.as_manager()

    class Meta:
        db_table = "watering_session"
        get_latest_by = ["created_time", ]
        managed = False

    def __repr__(self):
        optional_end = "ongoing" if self.is_running else self.session_end.isoformat()
        return '<WateringSession ({start} - {end})>'.format(start=self.session_start.isoformat(),
                                                            end=optional_end)

    def __unicode__(self):
        optional_end = "ongoing" if self.is_running else self.session_end.isoformat()
        return "watering session from {start} to {end}".format(start=self.session_start.isoformat(),
                                                               end=optional_end)

    @property
    def gallons(self):
        minutes = self.length / 60.0
        return minutes * GALLONS_PER_MINUTE

    @property
    def length(self):
        """
        :return: An integer, the number of seconds the session lasted (or if it's still going, how long).
        """
        optional_end = now() if self.is_running else self.session_end
        return int(math.ceil((optional_end - self.session_start).total_seconds()))

    @property
    def length_label(self):
        """
        :return: A human-readable description of the length of the session.
        """
        seconds = self.length
        days, rem = divmod(seconds, 86400)
        hours, rem = divmod(rem, 3600)
        minutes, seconds = divmod(rem, 60)
        if seconds < 1: seconds = 1
        locals_ = locals()
        magnitudes_str = ("{n} {magnitude}".format(n=int(locals_[magnitude]), magnitude=magnitude)
                          for magnitude in ("days", "hours", "minutes", "seconds") if locals_[magnitude])
        eta_str = ", ".join(magnitudes_str)
        return eta_str

    @property
    def is_running(self):
        """
        :return: Is the session still running?
        """
        return not bool(self.session_end)

    @property
    def valve_number(self):
        return self.device_identifier + 1
