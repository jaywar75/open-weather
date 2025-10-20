# Open Weather MCP Client

This project demonstrates how to use the OpenWeather MCP server in a Python application via Docker.

## Setup

1. Get OpenWeatherMap API key from https://openweathermap.org/api

2. Set the API key in .env file: OWM_API_KEY=your_key

3. Build the MCP server Docker image: ./build.sh

4. Install dependencies: pip install -e .

5. Run the client: python client.py

## Requirements

- Python 3.8+
- Docker
- OpenWeatherMap API key

## Project Structure

- `client.py`: Main client application that connects to the MCP server
- `pyproject.toml`: Project configuration and dependencies
- `build.sh`: Script to build the MCP server Docker image
- `.env`: Environment variables (API key)
- `.gitignore`: Git ignore file