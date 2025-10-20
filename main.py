from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
import json
from datetime import datetime
from models import WeatherData
from database import get_db
import asyncio
import os
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()

app = FastAPI(title="OpenWeather MCP API", version="1.0.0")

class WeatherRequest(BaseModel):
    city: str
    units: Optional[str] = "c"
    lang: Optional[str] = "en"

class WeatherResponse(BaseModel):
    id: int
    city: str
    temperature: float
    temperature_unit: str
    conditions: str
    humidity: int
    pressure: float
    wind_speed: float
    wind_direction: float
    sunrise: datetime
    sunset: datetime
    forecast_data: str
    created_at: datetime

async def get_weather_data(city: str, units: str = "c", lang: str = "en"):
    api_key = os.getenv("OWM_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="API key not set")

    server_params = StdioServerParameters(
        command="docker",
        args=["run", "--rm", "-i", "-e", f"OWM_API_KEY={api_key}", "mcp-weather"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool("weather", {"city": city, "units": units, "lang": lang})
            return result.content[0].text

@app.post("/weather", response_model=WeatherResponse)
async def fetch_weather(request: WeatherRequest, db: Session = Depends(get_db)):
    try:
        weather_text = await get_weather_data(request.city, request.units, request.lang)
        # Parse the text to extract data (simplified, in real app use proper parsing)
        # For now, store the raw text
        weather_entry = WeatherData(
            city=request.city,
            temperature=20.0,  # placeholder
            temperature_unit=request.units,
            conditions=weather_text[:200],  # placeholder
            humidity=50,
            pressure=1013.0,
            wind_speed=5.0,
            wind_direction=180.0,
            sunrise=datetime.utcnow(),
            sunset=datetime.utcnow(),
            forecast_data=weather_text
        )
        db.add(weather_entry)
        db.commit()
        db.refresh(weather_entry)
        return WeatherResponse(**weather_entry.__dict__)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/weather/history", response_model=List[WeatherResponse])
def get_weather_history(city: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(WeatherData)
    if city:
        query = query.filter(WeatherData.city == city)
    return [WeatherResponse(**item.__dict__) for item in query.all()]