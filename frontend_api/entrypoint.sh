#!/bin/sh

# Wait for database to be ready
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "db" -U "$POSTGRES_USER" -d "frontend_db" -c '\q'; do
  echo "Postgres is unavailable - sleeping"
  sleep 1
done

echo "Postgres is up - executing migrations"

export FLASK_APP=run.py

# Create migrations directory if it doesn't exist
if [ ! -d "migrations" ]; then
    flask db init
fi

# Generate migration if there are changes
flask db migrate -m "Auto-migration"

# Apply migrations
flask db upgrade

exec flask run --host=0.0.0.0 --port=5000