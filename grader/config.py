import os
from dotenv import load_dotenv
from os.path import dirname, join

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

SECRET_KEY = os.environ.get('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
PUSHER_APP_ID = os.environ.get('PUSHER_APP_ID')
PUSHER_KEY = os.environ.get('PUSHER_KEY')
PUSHER_SECRET = os.environ.get('PUSHER_SECRET')
PUSHER_CLUSTER = os.environ.get('PUSHER_CLUSTER')
