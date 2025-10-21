FROM python:3.11-slim

# Install Docker CLI
RUN apt-get update && apt-get install -y docker.io && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Copy project files
COPY . /app

WORKDIR /app

# Install dependencies
RUN uv sync

# Run the client
CMD ["uv", "run", "python", "client.py"]