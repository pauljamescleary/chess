from flask import Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import argon2

app = Flask(__name__)
app.config.from_pyfile('settings.py')

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)
pwd_context = argon2
