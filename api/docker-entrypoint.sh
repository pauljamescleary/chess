#!/bin/sh
set -e

echo "SQLALCHEMY_DATABASE_URI = $SQLALCHEMY_DATABASE_URI"

echo "Files..."
ls -al

echo "Running migrations..."
flask db upgrade

echo "Starting app..."
flask run --host=0.0.0.0

# Not sure why we want to run gunicorn here???
# gunicorn -c gunicorn.config.py wsgi:app
