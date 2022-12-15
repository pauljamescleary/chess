#!/bin/sh
set -e

echo "FLASK_SQLALCHEMY_DATABASE_URI = $FLASK_SQLALCHEMY_DATABASE_URI"

echo "Files..."
ls -al

export FLASK_APP="chess"

echo "Running migrations..."
flask db upgrade

echo "Starting app..."
flask run --host=0.0.0.0

# Not sure why we want to run gunicorn here???
# gunicorn -c gunicorn.config.py wsgi:app
