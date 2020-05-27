from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, BigInteger, DateTime, Date, Float, String, \
    ForeignKey, Text

Base = declarative_base()


class WeatherStation(Base):
    __tablename__ = "weather_station"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(Text, nullable=False)
    lat = Column(Float, nullable=False)
    long = Column(Float, nullable=False)
    abbrv = Column(String, nullable=False)


class HourlyForecast(Base):
    __tablename__ = "hourly_forecast"
    id = Column(Integer, primary_key=True, nullable=False)
    dt_fetched = Column(DateTime, nullable=False)
    dt_for = Column(DateTime, nullable=False)
    temp = Column(Float)
    app_temp = Column(Float)
    dwpt = Column(Float)
    rh = Column(Float)
    wspd = Column(Float)
    wdir = Column(Float)
    wc = Column(Float)
    clds = Column(String)
    vis = Column(Float)
    pres = Column(Float)
    uv_idx = Column(Float)
    prcp = Column(Float)
    heat_idx = Column(Float)

    weather_station_id = Column(Integer, ForeignKey("weather_station.id"))

    # relationship allows us to access the underlying station table when we have a row instance of `HourlyForecast`
    weather_station = relationship(WeatherStation, foreign_keys=[weather_station_id])


class DailyForecast(Base):
    __tablename__ = "daily_forecast"
    id = Column(Integer, primary_key=True, nullable=False)
    dt_fetched = Column(DateTime, nullable=False)
    dt_for = Column(DateTime, nullable=False)
    tmin = Column(Float)
    tmax = Column(Float)
    app_tmin = Column(Float)
    app_tmax = Column(Float)
    wspeed = Column(Float)
    wdir = Column(Float)
    prcp = Column(Float)
    rh = Column(Float)

    weather_station_id = Column(Integer, ForeignKey("weather_station.id"))
    weather_station = relationship(WeatherStation, foreign_keys=[weather_station_id])