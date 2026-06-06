# Use official Python runtime as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies including curl for health checks, and nginx for the API Gateway
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Remove default nginx config and link the monolithic config
RUN rm /etc/nginx/conf.d/default.conf || true
RUN cp nginx.monolith.conf /etc/nginx/nginx.conf

# Make the start script executable
RUN chmod +x start.sh

# Expose Nginx port
EXPOSE 80

# Command to run the application using the monolith startup script
CMD ["./start.sh"]
