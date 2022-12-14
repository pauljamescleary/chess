from dotenv import load_dotenv
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import argon2


# This is accessed elsewhere, so initialize here
# to enable access as a global variable
db = SQLAlchemy()

# Used for hashing passwords / salt
password_hasher = argon2

def create_app(env=None):
    app = Flask(__name__, instance_relative_config=False)

    print(f"*** ENV({env}) ***")
    if env:
        load_dotenv(f".env.{env}")

    # Loads environment variables / settings
    app.config.from_pyfile('settings.py')

    print(app.config['SQLALCHEMY_DATABASE_URI'])

    # Creates the database layer
    db.init_app(app)

    # Enables creation of migrations
    Migrate(app, db)    

    # Used for marshalling data to/from JSON
    Marshmallow(app)

    # Sets up the API routes
    from . import routes
    routes.configure_routes(app, db, password_hasher)

    return app

if __name__ == '__main__':
    print("*** IN INIT ***")
    create_app().run(debug=True, host='0.0.0.0')    
