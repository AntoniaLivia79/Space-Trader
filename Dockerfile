# Use lightweight Ubuntu image
FROM ubuntu:22.04

# Set up environment
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Install Python and required dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-dev \
    sqlite3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /app

# Copy requirements (if you have a requirements.txt)
# COPY requirements.txt .
# RUN pip3 install -r requirements.txt

# Install required packages
RUN pip3 install bcrypt

# Copy application code
COPY server.py .
COPY game.py .

# Create directory for database
RUN mkdir -p /data
VOLUME ["/data"]

# Set environment variable for database path
ENV DB_PATH=/data/space_trader.db

# Expose the port the app runs on
EXPOSE 3000

# Command to run the application
CMD ["python3", "server.py"]