#!/bin/sh

echo "Starting Django..."
gunicorn app.wsgi:application --bind 0.0.0.0:8000 &

echo "Starting Celery..."
celery -A app worker -l info

wait
