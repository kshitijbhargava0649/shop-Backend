import os
from datetime import timedelta

class Config:
    # Flask config
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')
    
    # JWT config
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'your-jwt-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
    # MongoDB config
    MONGODB_SETTINGS = {
        'db': 'shop',
        'host': 'mongodb://localhost:27017/shop'
    }
    
    # PostgreSQL config
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://username:password@localhost:5432/shop_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False 