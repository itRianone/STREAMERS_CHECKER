import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.env')
load_dotenv(dotenv_path=env_path)

#var's
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
SECRET_KEY = os.getenv('SECRET_KEY')
CLIENT_ID = os.getenv('CLIENT_ID')
APP_ACCESS_TOKEN = os.getenv('APP_ACCESS_TOKEN')
API_KEY = os.getenv('API_KEY')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
