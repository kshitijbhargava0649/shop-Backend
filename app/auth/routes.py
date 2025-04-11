import traceback
from flask import request
from flask_restx import Namespace, Resource
from flask_jwt_extended import create_access_token, jwt_required
from .controller import (
    create_user, authenticate_user, get_current_user
)
from .models import init_models

api = Namespace('auth', description='Authentication related endpoints')
models = init_models(api)

@api.route('/signup')
class Signup(Resource):
    @api.expect(models['signup_model'])
    def post(self):
        """Create a new user account"""
        try:
            data = request.json
            user = create_user(data)
            token = create_access_token(identity=str(user.id))  # timeout?
            return {
                'token': token,
                'user': user.to_dict()
            }, 201
        except Exception as e:
            return {'error': str(e)}, 400

@api.route('/signin')
class Login(Resource):
    @api.expect(models['login_model'])
    def post(self):
        """Authenticate user and get JWT token"""
        try:
            data = request.json
            
            # Basic validation
            if not data.get('email') or not data.get('password'):
                return {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Email and password are required'
                }, 400
            
            user = authenticate_user(data['email'], data['password'])
            if not user:
                return {
                    'code': 'INVALID_CREDENTIALS',
                    'message': 'Invalid email or password'
                }, 401
            
            token = create_access_token(identity=str(user.id))
            return {
                'token': token,
                'user': user.to_dict()
            }, 200
            
        except Exception as e:
            # Log the actual error for debugging
            print(f"Login error: {str(e)}")
            return {
                'code': 'SERVER_ERROR',
                'message': 'An unexpected error occurred'
            }, 500

@api.route('/me')
class CurrentUser(Resource):
    @jwt_required()
    def get(self):
        """Get current authenticated user's information"""
        try:
            user = get_current_user()
            if not user:
                return {'error': 'User not found'}, 404
            return user.to_dict()
        except Exception as e:
            return {'error': str(e)}, 500 