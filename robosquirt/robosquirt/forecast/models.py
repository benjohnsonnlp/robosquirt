import ciso8601
import logging
from sqlalchemy import Column, Integer, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base

from .nws import ForecastEndpoint

Base = declarative_base()

logger = logging.getLogger("robosquirt")


class UserSettings(Base):
    __tablename__ = "geo_usersettings"

    id = Column(Integer, primary_key=True)
    location_id = Column(Integer)
    email = Column(Text)
    nws_daily_endpoint = Column(Text)
    nws_hourly_endpoint = Column(Text)


class Forecast(Base):
    __tablename__ = "forecasts"

    period_index = Column(Integer, primary_key=True)
    start = Column(DateTime(timezone=True), nullable=False)
    end = Column(DateTime(timezone=True), nullable=False)
    forecast_long = Column(Text, nullable=False)
    forecast_short = Column(Text, nullable=False)
    temperature = Column(Integer, nullable=False)
    is_daytime = Column(Boolean, nullable=False)
    precipitation_probability = Column(Text, nullable=False)
    icon_type = Column(Text, nullable=False)

    def __repr__(self):
        return '<Forecast {index} ({start} - {end})>'.format(index=self.period_index,
                                                             start=self.start.isoformat(),
                                                             end=self.end.isoformat())

    @classmethod
    def reload_nws_forecasts(cls, session):
        user_settings = session.query(UserSettings).one()
        forecast_endpoint = ForecastEndpoint(user_settings.nws_hourly_endpoint)
        removed_count = 0
        for forecast in session.query(cls).all():
            session.delete(forecast)
            removed_count += 1
        session.flush()
        forecast_periods = []
        for period in forecast_endpoint.periods:
            forecast_periods.append(Forecast(period_index=period["number"],
                                             start=ciso8601.parse_datetime(period["startTime"]),
                                             end=ciso8601.parse_datetime(period["endTime"]),
                                             is_daytime=period["isDaytime"],
                                             temperature=period["temperature"],
                                             forecast_short=period["shortForecast"],
                                             forecast_long=period["detailedForecast"],
                                             precipitation_probability=period["precipitationProbability"],
                                             icon_type=period["iconType"]))
        session.add_all(forecast_periods)
        session.commit()
        added_count = len(forecast_periods)
        logger.info("Removed {} existing forecasts and saved {} new forecasts.".format(removed_count,added_count))
