#!/bin/sh

# Wait for PostgreSQL to be ready before running the Django server
# Replace 'postgres' with your PostgreSQL service name in docker-compose.yml
# Change the '5' to a higher value if you encounter connection issues
# This helps ensure that the database is up before starting Django
echo "insideentrypoint"
python django/manage.py migrate &&
python django/manage.py runserver 0.0.0.0:8000