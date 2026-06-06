#!/bin/bash
set -e

echo "Starting Auth Service on port 8001..."
cd /app/auth-service/src
uvicorn main:app --host 127.0.0.1 --port 8001 &

echo "Starting User Service on port 8002..."
cd /app/user-service/src
uvicorn main:app --host 127.0.0.1 --port 8002 &

echo "Starting Job Catalog Service on port 8003..."
cd /app/job-catalog-service/src
uvicorn main:app --host 127.0.0.1 --port 8003 &

echo "Starting Tracker Service on port 8004..."
cd /app/tracker-service/src
uvicorn main:app --host 127.0.0.1 --port 8004 &

echo "Starting AI Service on port 8005..."
cd /app/ai-service/src
uvicorn main:app --host 127.0.0.1 --port 8005 &

echo "Starting NGINX API Gateway on port 80..."
# Start Nginx in the foreground so the container stays alive
nginx -g "daemon off;"
