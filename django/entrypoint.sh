#!/bin/sh

# Wait for PostgreSQL to be ready before running the Django server
# Replace 'postgres' with your PostgreSQL service name in docker-compose.yml
# Change the '5' to a higher value if you encounter connection issues
# This helps ensure that the database is up before starting Django
until PGPASSWORD=$DB_PASSWORD psql -h "postgres" -U "$DB_USER" -d "$DB_NAME" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 5
done

# Apply database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start the Django development server
python manage.py runserver 0.0.0.0:8000