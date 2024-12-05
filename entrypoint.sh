#!/bin/sh

# Check if migrations should be run
if [ "$RUN_MIGRATIONS" = "true" ]; then
    # Run database migrations
    echo "Running database migrations..."
    python manage.py migrate  || { echo "Migrations failed"; exit 1; }
else
    echo "Skipping database migrations..."
fi

# Keep the container running (optional, if you want to debug or keep the container alive)
echo "Entrypoint script executed. Container is now ready."
exec "$@"
