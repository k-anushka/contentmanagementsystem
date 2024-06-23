#!/bin/sh

# Wait for MySQL to be ready
# while ! mysqladmin ping -h"$DB_HOST" --silent; do
#     echo "Waiting for database connection..."
#     sleep 2
# done

# Apply database migrations
echo "Applying database migrations..."
python manage.py makemigrations
python manage.py migrate

# Create a superuser if it doesn't exist
echo "Creating superuser..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword')
END

# Start the Django server
echo "Starting server..."
exec "$@"
