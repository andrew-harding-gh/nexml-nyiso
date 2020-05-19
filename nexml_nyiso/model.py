from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, BigInteger, DateTime, Date, Float, String, \
    ForeignKey, Text

Base = declarative_base()


class WeatherStation(Base):
    __tablename__ = "weather_station"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(Text, nullable=False)


class HourlyForecast(Base):
    __tablename__ = "hourly_forecast"
    id = Column(Integer, primary_key=True, nullable=False)
    temp = Column(Float, nullable=False)
    date_for = Column(DateTime, nullable=False)
    weather_station_id = Column(Integer, ForeignKey("weather_station.id"))

    # relationship allows us to access the underlying station table when we have a row instance of `HourlyForecast`
    weather_station = relationship(WeatherStation, foreign_keys=[weather_station_id])
