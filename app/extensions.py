from flask_jwt_extended import JWTManager
from mongoengine import connect
from flask_sqlalchemy import SQLAlchemy

# Initialize extensions
jwt = JWTManager()
postgres_db = SQLAlchemy()  # For PostgreSQL
db = postgres_db  # Alias for backward compatibility 