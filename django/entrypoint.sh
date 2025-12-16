#!/bin/bash
echo "Creating Migrations..."
python manage.py makemigrations
echo ====================================

echo "Starting Migrations..."
python manage.py migrate
echo ====================================

echo "Starting Server..."
python -m uvicorn c2s.asgi:application --host 0.0.0.0 