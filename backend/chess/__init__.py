import os
from flask import Flask, abort, jsonify, request, session
from sqlalchemy.exc import IntegrityError
from flask_httpauth import HTTPBasicAuth
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import argon2

app = Flask(__name__)

# Loads environment variables prefixed with FLASK_
app.config.from_prefixed_env()

# Initializes the db to use with the app
db = SQLAlchemy(app)
print(app.config['SQLALCHEMY_DATABASE_URI'])

# For password salt and secrets
password_hasher = argon2

# Enables creation of migrations
migrate = Migrate(app, db)

# Apply migrations if in sqllite
db_url = app.config['SQLALCHEMY_DATABASE_URI']
if db_url.startswith('sqlite'):
    # We MUST import chess models here
    # otherwise nothing will happen in test mode
    import chess.models
    with app.app_context():
        db.create_all()

# Used for authenticating the caller
auth = HTTPBasicAuth()

# Configure the endpoints
# Make sure we do the import here, otherwise we get python errors
import chess.routes
