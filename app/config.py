import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
    FLASK_APP = os.getenv('FLASK_APP', 'backend/run.py')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_DEBUG = int(os.getenv('FLASK_DEBUG', 1))

    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-jwt-secret')
    # JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600)))

    # MongoDB Configuration
    MONGODB_SETTINGS = {
        'db': os.getenv('MONGO_DB', 'shop_db'),
        'host': os.getenv('MONGO_URI', 'mongodb://localhost:27017/shop_db'),
        'username': os.getenv('MONGO_INITDB_ROOT_USERNAME'),
        'password': os.getenv('MONGO_INITDB_ROOT_PASSWORD'),
        'authentication_source': 'admin'
    }

    # PostgreSQL Configuration
    POSTGRES_DB = os.getenv('POSTGRES_DB', 'shop_db')
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'shop_user')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'shop_password')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT = int(os.getenv('POSTGRES_PORT', 5432))
    
    SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Shopify Configuration
    SHOPIFY_SHOP_NAME = os.getenv('SHOPIFY_SHOP_NAME', 'your-shop-name')
    SHOPIFY_ACCESS_TOKEN = os.getenv('SHOPIFY_ACCESS_TOKEN', 'your-access-token')
    SHOPIFY_API_VERSION = os.getenv('SHOPIFY_API_VERSION', '2024-01')

