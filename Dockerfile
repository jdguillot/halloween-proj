# Use Python slim image for Raspberry Pi
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY templates/ templates/


# Expose port 5000
EXPOSE 5000

# Set environment variables with defaults
ENV MQTT_BROKER=localhost
ENV MQTT_PORT=1883
ENV MQTT_TOPIC=home/buttons
ENV MQTT_USERNAME=
ENV MQTT_PASSWORD=

# Run the application
CMD ["python", "app.py"]
