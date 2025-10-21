'use client';

import { useState } from 'react';

interface WeatherData {
  id: number;
  city: string;
  state: string;
  zip_code: string;
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

interface ForecastEntry {
  dateTime: string;
  conditions: string;
  temp: number;
}

export default function Home() {
  const [city, setCity] = useState('');
  const [state, setState] = useState('');
  const [zipCode, setZipCode] = useState('');
  const [units, setUnits] = useState('c');
  const [lang, setLang] = useState('en');
  const [weather, setWeather] = useState<WeatherData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const parseForecast = (forecastData: string): ForecastEntry[] => {
    const entries: ForecastEntry[] = [];
    const forecastSection = forecastData.split('Weather Forecast for')[1];
    if (!forecastSection) return entries;

    const blocks = forecastSection.split('Date & Time:').slice(1);
    
    for (const block of blocks) {
      const dateTimeMatch = block.match(/^(.+?)$/m);
      const conditionsMatch = block.match(/Conditions:\s+(.+?)$/m);
      const tempMatch = block.match(/Temp:\s+([\d.]+)/);
      
      if (dateTimeMatch && conditionsMatch && tempMatch) {
        entries.push({
          dateTime: dateTimeMatch[1].trim(),
          conditions: conditionsMatch[1].trim(),
          temp: parseFloat(tempMatch[1])
        });
      }
    }
    
    return entries;
  };

  const fetchWeather = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await fetch('http://localhost:8000/weather', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ city, state, zip_code: zipCode, units, lang }),
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
        <h1 className="text-4xl font-bold text-white mb-8 text-center">OpenWeather Client via MCP Service</h1>

        <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
          <div className="grid grid-cols-1 md:grid-cols-6 gap-4 mb-4">
            <input
              type="text"
              placeholder="City (e.g., Raleigh, New York, London)"
              value={city}
              onChange={(e) => setCity(e.target.value)}
              className="p-3 border-2 border-gray-800 rounded text-black font-medium placeholder-gray-600 focus:border-blue-700 focus:outline-none bg-white"
            />
            <input
              type="text"
              placeholder="State (e.g., NC, OH, FL)"
              value={state}
              onChange={(e) => setState(e.target.value)}
              className="p-3 border-2 border-gray-800 rounded text-black font-medium placeholder-gray-600 focus:border-blue-700 focus:outline-none bg-white"
              maxLength={2}
            />
            <input
              type="text"
              placeholder="Zip Code (e.g., 27502)"
              value={zipCode}
              onChange={(e) => setZipCode(e.target.value)}
              className="p-3 border-2 border-gray-800 rounded text-black font-medium placeholder-gray-600 focus:border-blue-700 focus:outline-none bg-white"
              maxLength={5}
              pattern="[0-9]*"
            />
            <select value={units} onChange={(e) => setUnits(e.target.value)} className="p-3 border-2 border-gray-800 rounded text-black font-medium focus:border-blue-700 focus:outline-none bg-white">
              <option value="c">Celsius</option>
              <option value="f">Fahrenheit</option>
              <option value="k">Kelvin</option>
            </select>
            <select value={lang} onChange={(e) => setLang(e.target.value)} className="p-3 border-2 border-gray-800 rounded text-black font-medium focus:border-blue-700 focus:outline-none bg-white">
              <option value="en">English</option>
              <option value="de">German</option>
              <option value="fr">French</option>
            </select>
            <button
              onClick={fetchWeather}
              disabled={loading}
              className="bg-blue-600 text-white p-3 rounded hover:bg-blue-700 disabled:opacity-50 font-bold border-2 border-blue-800"
            >
              {loading ? 'Loading...' : 'Get Weather'}
            </button>
          </div>

          {error && <p className="text-red-700 font-bold mb-4 text-lg">{error}</p>}

          {weather && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-gray-50 p-4 rounded border-2 border-gray-700">
                <h2 className="text-2xl font-bold mb-4 text-black">{weather.city} - Current Weather</h2>
                <p className="text-black mb-3 text-base"><span className="font-bold">Temperature:</span> {weather.temperature}°{weather.temperature_unit.toUpperCase()}</p>
                <p className="text-black mb-3 text-base"><span className="font-bold">Conditions:</span> {weather.conditions}</p>
                <p className="text-black mb-3 text-base"><span className="font-bold">Humidity:</span> {weather.humidity}%</p>
                <p className="text-black mb-3 text-base"><span className="font-bold">Pressure:</span> {weather.pressure} hPa</p>
                <p className="text-black mb-3 text-base"><span className="font-bold">Wind:</span> {weather.wind_speed} m/s at {weather.wind_direction}°</p>
                <p className="text-black mb-3 text-base"><span className="font-bold">Sunrise:</span> {new Date(weather.sunrise).toLocaleTimeString()}</p>
                <p className="text-black mb-3 text-base"><span className="font-bold">Sunset:</span> {new Date(weather.sunset).toLocaleTimeString()}</p>
              </div>
              <div className="bg-gray-50 p-4 rounded border-2 border-gray-700">
                <h2 className="text-2xl font-bold mb-4 text-black">Forecast</h2>
                <div className="space-y-3 max-h-96 overflow-y-auto">
                  {parseForecast(weather.forecast_data).map((entry, index) => {
                    const date = new Date(entry.dateTime);
                    const timeStr = date.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true });
                    const dateStr = date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
                    
                    return (
                      <div key={index} className="bg-white p-3 rounded border-2 border-gray-600">
                        <div className="flex justify-between items-center">
                          <div>
                            <p className="text-black font-bold text-base">{dateStr} at {timeStr}</p>
                            <p className="text-black text-sm">{entry.conditions}</p>
                          </div>
                          <div className="text-right">
                            <p className="text-black font-bold text-2xl">{entry.temp.toFixed(1)}°{weather.temperature_unit.toUpperCase()}</p>
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
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
