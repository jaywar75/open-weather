# Open Weather MCP Client

A full-stack application for fetching and displaying weather data using the OpenWeather MCP server, with data archiving in PostgreSQL.

## Features

- **Backend**: FastAPI server with PostgreSQL for data persistence
- **Frontend**: Next.js with TypeScript, TSX, and Tailwind CSS
- **MCP Integration**: Connects to OpenWeather MCP server via Docker
- **Data Archiving**: Weather results stored in PostgreSQL for historical analysis

## Architecture

- **Database**: PostgreSQL for weather data storage
- **Backend**: Python/FastAPI for API endpoints and MCP client integration
- **Frontend**: React/Next.js for user interface
- **MCP Server**: Dockerized OpenWeather MCP server for weather data retrieval

## Setup

1. **Prerequisites**:
   - Docker and Docker Compose
   - OpenWeatherMap API key

2. **Clone and configure**:
   ```bash
   git clone https://github.com/jaywar75/open-weather.git
   cd open-weather
   cp .env.example .env  # Add your OWM_API_KEY
   ```

3. **Build and run**:
   ```bash
   docker-compose up --build
   ```

4. **Access**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## API Endpoints

- `POST /weather`: Fetch and store weather data
- `GET /weather/history`: Retrieve historical weather data

## Usage

1. Open the frontend at http://localhost:3000
2. Enter a city name, select units and language
3. Click "Get Weather" to fetch and display data
4. Data is automatically archived in PostgreSQL

## Development

- Backend: `uv run uvicorn main:app --reload`
- Frontend: `cd frontend && npm run dev`
- Database: Access via `docker-compose exec db psql -U user -d openweather`

## Technologies

- **Backend**: Python, FastAPI, SQLAlchemy, PostgreSQL
- **Frontend**: TypeScript, React, Next.js, Tailwind CSS
- **Infrastructure**: Docker, Docker Compose
- **MCP**: Model Context Protocol for AI tool integration