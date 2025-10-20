from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class WeatherData(Base):
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True)
    temperature = Column(Float)
    temperature_unit = Column(String)
    conditions = Column(Text)
    humidity = Column(Integer)
    pressure = Column(Float)
    wind_speed = Column(Float)
    wind_direction = Column(Float)
    sunrise = Column(DateTime)
    sunset = Column(DateTime)
    forecast_data = Column(Text)  # JSON string for forecast
    created_at = Column(DateTime, default=datetime.utcnow)