'use client';

import { useState } from 'react';

interface WeatherData {
  id: number;
  city: string;
  temperature: number;
  temperature_unit: string;
  conditions: string;
  humidity: number;
  pressure: number;
  wind_speed: number;
  wind_direction: number;
  sunrise: string;
  sunset: string;
  forecast_data: string;
  created_at: string;
}

export default function Home() {
  const [city, setCity] = useState('');
  const [units, setUnits] = useState('c');
  const [lang, setLang] = useState('en');
  const [weather, setWeather] = useState<WeatherData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchWeather = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await fetch('http://localhost:8000/weather', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ city, units, lang }),
      });
      if (!response.ok) throw new Error('Failed to fetch weather');
      const data: WeatherData = await response.json();
      setWeather(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-400 to-blue-600 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-white mb-8 text-center">OpenWeather MCP Client</h1>

        <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
            <input
              type="text"
              placeholder="City"
              value={city}
              onChange={(e) => setCity(e.target.value)}
              className="p-2 border rounded"
            />
            <select value={units} onChange={(e) => setUnits(e.target.value)} className="p-2 border rounded">
              <option value="c">Celsius</option>
              <option value="f">Fahrenheit</option>
              <option value="k">Kelvin</option>
            </select>
            <select value={lang} onChange={(e) => setLang(e.target.value)} className="p-2 border rounded">
              <option value="en">English</option>
              <option value="de">German</option>
              <option value="fr">French</option>
            </select>
            <button
              onClick={fetchWeather}
              disabled={loading}
              className="bg-blue-500 text-white p-2 rounded hover:bg-blue-600 disabled:opacity-50"
            >
              {loading ? 'Loading...' : 'Get Weather'}
            </button>
          </div>

          {error && <p className="text-red-500 mb-4">{error}</p>}

          {weather && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h2 className="text-2xl font-semibold mb-4">{weather.city} - Current Weather</h2>
                <p>Temperature: {weather.temperature}°{weather.temperature_unit.toUpperCase()}</p>
                <p>Conditions: {weather.conditions}</p>
                <p>Humidity: {weather.humidity}%</p>
                <p>Pressure: {weather.pressure} hPa</p>
                <p>Wind: {weather.wind_speed} m/s at {weather.wind_direction}°</p>
                <p>Sunrise: {new Date(weather.sunrise).toLocaleTimeString()}</p>
                <p>Sunset: {new Date(weather.sunset).toLocaleTimeString()}</p>
              </div>
              <div>
                <h2 className="text-2xl font-semibold mb-4">Forecast</h2>
                <pre className="whitespace-pre-wrap text-sm">{weather.forecast_data}</pre>
              </div>
            </div>
          )}
        </div>

        <div className="text-center text-white">
          <p>Data is archived in PostgreSQL for historical analysis.</p>
        </div>
      </div>
    </div>
  );
}
