import bcrypt
from datetime import datetime, timedelta
from typing import Optional, Dict
from flask import current_app
from flask_jwt_extended import create_access_token, get_jwt_identity
from .models import User
from app.extensions import db
from app.events.models import Event
from app.events.services import log_event 

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )

def get_password_hash(password: str) -> str:
    """Generate password hash"""
    return bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')

def authenticate_user(email: str, password: str) -> Optional[User]:
    """Authenticate user and return user object if valid"""
    try:
        user = User.objects(email=email).first()
        if not user or not verify_password(password, user.hashed_password):
            return None
        
        # Log successful login event
        # log_event('LOGIN', 'AUTH', str(user.id))
        
        return user
    except Exception as e:
        current_app.logger.error(f"Authentication error: {str(e)}")
        return None

def create_user(user_data: Dict) -> User:
    """Create new user"""
    try:
        # Check if user already exists
        if User.objects(email=user_data['email']).first():
            raise ValueError("Email already registered")

        # Hash the password
        hashed_password = get_password_hash(user_data['password'])
        
        # Create new user
        user = User(
            name=user_data['name'],
            email=user_data['email'],
            hashed_password=hashed_password
        )
        user.save()
        
        # Log user creation event
        # log_event('CREATE', 'USER', str(user.id))
        
        return user
    except Exception as e:
        current_app.logger.error(f"User creation error: {str(e)}")
        raise

def get_current_user() -> User:
    """Get current user from token"""
    try:
        user_id = get_jwt_identity()
        if not user_id:
            return None
        
        user = User.objects(id=user_id).first()
        if not user:
            return None
            
        # Log token validation event
        # log_event('VALIDATE', 'TOKEN', str(user.id))
        
        return user
    except Exception as e:
        current_app.logger.error(f"Token validation error: {str(e)}")
        return None 