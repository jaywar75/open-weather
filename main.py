from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import re
import traceback
from datetime import datetime, timezone
from dotenv import load_dotenv
from models import WeatherData
from database import get_db
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()

app = FastAPI(title="OpenWeather MCP API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4444"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def normalize_units(units: Optional[str]) -> str:
    if not units:
        return "metric"
    mapping = {"c": "metric", "f": "imperial", "k": "standard"}
    return mapping.get(units.lower(), units)


def parse_weather_text(weather_text: str) -> Dict[str, Any]:
    data: Dict[str, Any] = {}
    current_section_match = re.search(r"Current weather for .*?:\n(.*?)(?:\n\n|\Z)", weather_text, re.DOTALL)
    current_section = current_section_match.group(1) if current_section_match else weather_text

    def extract_float(pattern: str, section: str = current_section) -> Optional[float]:
        match = re.search(pattern, section)
        return float(match.group(1)) if match else None

    def extract_int(pattern: str, section: str = current_section) -> Optional[int]:
        match = re.search(pattern, section)
        return int(match.group(1)) if match else None

    def extract_str(pattern: str, section: str = current_section) -> Optional[str]:
        match = re.search(pattern, section)
        return match.group(1).strip() if match else None

    data["conditions"] = extract_str(r"Conditions:\s+(.+)")
    data["temperature"] = extract_float(r"Now:\s*([\d.]+)")
    data["temperature_unit_text"] = extract_str(r"Now:\s*[\d.]+\s+([A-Za-z]+)")
    data["humidity"] = extract_int(r"Humidity:\s*(\d+)")
    data["pressure"] = extract_float(r"Pressure:\s*([\d.]+)")
    data["wind_speed"] = extract_float(r"Wind Speed:\s*([\d.]+)")
    data["wind_direction"] = extract_float(r"Wind Degree:\s*([\d.]+)")

    sunrise_unix = extract_int(r"Sunrise:\s*(\d+)\s+Unixtime")
    sunset_unix = extract_int(r"Sunset:\s*(\d+)\s+Unixtime")
    if sunrise_unix:
        data["sunrise"] = datetime.fromtimestamp(sunrise_unix, tz=timezone.utc)
    if sunset_unix:
        data["sunset"] = datetime.fromtimestamp(sunset_unix, tz=timezone.utc)

    return data


async def get_weather_data(city: str, units: str = "metric", lang: str = "en") -> str:
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
            result = await session.call_tool(
                "weather",
                {"city": city, "units": units, "lang": lang},
            )
            return result.content[0].text


class WeatherRequest(BaseModel):
    city: str
    state: Optional[str] = None
    zip_code: Optional[str] = None
    units: Optional[str] = "c"
    lang: Optional[str] = "en"


class WeatherResponse(BaseModel):
    id: int
    city: str
    state: Optional[str]
    zip_code: Optional[str]
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


@app.post("/weather", response_model=WeatherResponse)
async def fetch_weather(request: WeatherRequest, db: Session = Depends(get_db)):
    try:
        # MCP server expects single-letter codes: c, f, k
        mcp_units = (request.units or "c").lower()
        weather_text = await get_weather_data(request.city, mcp_units, request.lang or "en")
        parsed = parse_weather_text(weather_text)

        # Extract values from parsed weather data
        temperature = parsed.get("temperature", 20.0)
        humidity = parsed.get("humidity", 50)
        pressure = parsed.get("pressure", 1013.0)
        wind_speed = parsed.get("wind_speed", 5.0)
        wind_direction = parsed.get("wind_direction", 180.0)
        sunrise = parsed.get("sunrise", datetime.utcnow())
        sunset = parsed.get("sunset", datetime.utcnow())
        conditions = parsed.get("conditions", weather_text[:200])

        # Determine unit display based on MCP unit code
        if mcp_units == "f":
            temperature_unit_display = "F"
        elif mcp_units == "k":
            temperature_unit_display = "K"
        else:
            temperature_unit_display = "C"

        weather_entry = WeatherData(
            city=request.city,
            state=request.state,
            zip_code=request.zip_code,
            temperature=temperature,
            temperature_unit=temperature_unit_display,
            conditions=conditions,
            humidity=humidity,
            pressure=pressure,
            wind_speed=wind_speed,
            wind_direction=wind_direction,
            sunrise=sunrise,
            sunset=sunset,
            forecast_data=weather_text,
        )
        db.add(weather_entry)
        db.commit()
        db.refresh(weather_entry)
        return WeatherResponse(**weather_entry.__dict__)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/weather/history", response_model=List[WeatherResponse])
def get_weather_history(city: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(WeatherData)
    if city:
        query = query.filter(WeatherData.city == city)
    return [WeatherResponse(**item.__dict__) for item in query.all()]