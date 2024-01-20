#!/bin/bash

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate


python manage.py migrate --run-syncdb
python manage.py loaddata group.json users.json data.json

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000