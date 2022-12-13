from flask import Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import argon2

# This is accessed elsewhere, so initialize here
# to enable access as a global variable
db = SQLAlchemy()

def create_app(testing=False):
    app = Flask(__name__, instance_relative_config=False)

    if testing:
        # Load environment variables from the .env file
        # Those are used for testing
        dotenv.load_dotenv()

    # Loads environment variables / settings
    app.config.from_pyfile('settings.py')

    # Creates the database layer
    db.init_app(app)
    # db = SQLAlchemy(app)

    # Used for marshalling data to/from JSON
    Marshmallow(app)

    # Runs database migrations
    Migrate(app, db)

    # Used for hashing passwords / salt
    password_hasher = argon2

    # Sets up the API routes
    from . import routes
    routes.configure_routes(app, db, password_hasher)

    return app
