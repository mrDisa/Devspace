#!/bin/sh

echo "Waiting for PostgreSQL..."

until pg_isready -h db -U postgres
do
    sleep 1
done

echo "PostgreSQL is ready!"

echo "Running migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."

exec gunicorn rubl.wsgi:application \
    --bind 0.0.0.0:8000