import os
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
load_dotenv(os.path.join(BASE_DIR, '.env'))


class Settings:
    PROJECT_NAME = os.getenv('PROJECT_NAME', 'DATA_GATEWAY')
    DATABASE_URL = os.getenv('DATABASE_URL', '')


settings = Settings()

