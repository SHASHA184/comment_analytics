import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_API_URL = "http://database:8081"
AUTH_API_URL = "http://auth_service:8082"
GOOGLE_AI_API_KEY = os.getenv('GOOGLE_AI_API_KEY')