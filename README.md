# Open Weather MCP Client

This project demonstrates how to use the OpenWeather MCP server in a Python application via Docker.

## Setup

1. Get OpenWeatherMap API key from https://openweathermap.org/api

2. Set the API key in .env file: OWM_API_KEY=your_key

3. Build the MCP server Docker image: ./build.sh

4. Install dependencies: uv sync

5. Run the client: uv run python client.py (local) or docker-compose up (containerized)

## Usage

The client provides an interactive command-line interface:

- Enter a city name to get weather data
- Specify units: c (Celsius), f (Fahrenheit), k (Kelvin)
- Specify language (e.g., en, de, fr)
- Type 'quit' to exit

## Requirements

- Python 3.11+
- uv package manager
- Docker
- OpenWeatherMap API key

## Project Structure

- `client.py`: Interactive client application
- `pyproject.toml`: Project configuration and dependencies
- `uv.lock`: Locked dependencies
- `build.sh`: Script to build the MCP server Docker image
- `Dockerfile`: Container definition for the client
- `docker-compose.yml`: Orchestration for containerized run
- `.env`: Environment variables (API key)
- `.gitignore`: Git ignore file