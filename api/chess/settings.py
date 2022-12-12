from os import environ
from dotenv import load_dotenv 

load_dotenv()
SQLALCHEMY_DATABASE_URI = environ['APP_DATABASE_URL']
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = environ['APP_SECRET']
