from mongoengine import (
    Document, StringField, BooleanField,
    EmailField
)
from flask_restx import fields

class User(Document):
    name = StringField(required=True, max_length=100)
    email = EmailField(required=True, unique=True)
    hashed_password = StringField(required=True)
    is_active = BooleanField(default=True)

    meta = {
        'collection': 'identifier_users',
        'indexes': ['email']
    }

    def to_dict(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'email': self.email,
            'is_active': self.is_active
        }

def init_models(api):
    """Initialize API models for authentication endpoints"""
    
    # Request models
    signup_model = api.model('Signup', {
        'name': fields.String(required=True),
        'email': fields.String(required=True),
        'password': fields.String(required=True)
    })

    login_model = api.model('Login', {
        'email': fields.String(required=True),
        'password': fields.String(required=True)
    })

    # Response models
    user_model = api.model('User', {
        'id': fields.String,
        'name': fields.String,
        'email': fields.String
    })

    token_response = api.model('TokenResponse', {
        'token': fields.String,
        'user': fields.Nested(user_model)
    })

    return {
        'signup_model': signup_model,
        'login_model': login_model,
        'user_model': user_model,
        'token_response': token_response
    } 