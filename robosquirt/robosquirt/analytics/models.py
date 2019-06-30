"""
SQL Alchemy declarative classes representing the tables we'll store Robosquirt analytics in
"""
import logging
import math
from sqlalchemy import VARCHAR, Column, Integer, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property

from robosquirt.utils import utc_now

Base = declarative_base()


class WateringSession(Base):
    """
    A DB representation of a watering session (i.e a period of time when a valve was turned on then off).
    """
    __tablename__ = "watering_session"

    identifier = Column(VARCHAR(length=36), primary_key=True)
    created_time = Column(DateTime(timezone=True), default=utc_now)
    session_start = Column(DateTime(timezone=True), nullable=False)
    session_end = Column(DateTime(timezone=True))
    device_identifier = Column(Integer(), nullable=False)
    originator = Column(Text())
    reason = Column(Text())

    def __repr__(self):
        optional_end = "ongoing" if self.is_running else self.session_end.isoformat()
        return '<WateringSession ({start} - {end})>'.format(start=self.session_start.isoformat(),
                                                            end=optional_end)

    @hybrid_method
    def __len__(self):
        """
        :return: An integer, the number of seconds the session lasted (or if it's still going, how long).
        """
        optional_end = utc_now() if self.is_running else self.session_end
        return int(math.ceil((optional_end - self.session_start).total_seconds()))

    @hybrid_property
    def is_running(self):
        return not bool(self.session_end)

    @classmethod
    def delete_open_sessions(cls, session):
        removed_count = 0
        for watering_session in session.query(cls).filter(cls.session_end is None).all():
            session.delete(watering_session)
            removed_count += 1
        logging.info("Removed {} open sessions.".format(removed_count))
