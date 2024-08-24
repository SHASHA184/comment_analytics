import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
APP_API_URL = "http://app:8080"
DATABASE_API_URL = "http://database:8081"
AUTH_API_URL = "http://auth:8082"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30