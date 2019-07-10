import uuid

from moistmaster.utils import utc_now

from .models import WateringSession


class WateringSessionManager:

    def __init__(self, device_identifier):
        self.identifier = str(uuid.uuid4())
        self.device_identifier = device_identifier
        self._started = False
        self._ended = False
        self._session_pk = None

    def start(self):
        if self._started:
            raise ValueError('Session "{}" is already started.'.format(self.identifier))
        watering_session = WateringSession.objects.create(identifier=self.identifier,
                                                          device_identifier=self.device_identifier,
                                                          session_start=utc_now())
        self._started = True
        self._session_pk = watering_session.pk

    def end(self):
        if not self._started:
            raise ValueError('Session "{}" is hasn\'t been started yet.'.format(self.identifier))
        if self._ended:
            raise ValueError('Session "{}" is already ended.'.format(self.identifier))
        watering_session = WateringSession.objects.get(pk=self._session_pk)
        watering_session.session_end = utc_now()
        watering_session.save()
        self._ended = True
