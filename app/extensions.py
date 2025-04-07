from flask_jwt_extended import JWTManager
from mongoengine import connect
from flask_sqlalchemy import SQLAlchemy

# Initialize extensions
jwt = JWTManager()
db = SQLAlchemy()  # For PostgreSQL 