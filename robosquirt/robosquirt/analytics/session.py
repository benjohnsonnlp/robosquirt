import uuid

from sqlalchemy.orm import scoped_session

from robosquirt.analytics import models
from robosquirt.database import session_factory
from robosquirt.utils import utc_now


class WateringSession:

    def __init__(self, device_identifier):
        self.identifier = str(uuid.uuid4())
        self.device_identifier = device_identifier
        self.session = scoped_session(session_factory)
        self._started = False
        self._ended = False

    def start(self):
        if self._started:
            raise ValueError('Session "{}" is already started.'.format(self.identifier))
        watering_session = models.WateringSession(identifier=self.identifier,
                                                  device_identifier=self.device_identifier,
                                                  session_start=utc_now())
        self.session.add(watering_session)
        self.session.commit()
        self._started = True

    def end(self):
        if not self._started:
            raise ValueError('Session "{}" is hasn\'t been started yet.'.format(self.identifier))
        if self._ended:
            raise ValueError('Session "{}" is already ended.'.format(self.identifier))
        watering_session = self.session.query(models.WateringSession).get(self.identifier)
        watering_session.session_end = utc_now()
        self.session.commit()
        self._ended = True
