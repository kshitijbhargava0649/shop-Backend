import logging
from flask import Flask, request, make_response
from flask_cors import CORS
from mongoengine import connect, disconnect
from app.config import Config
from app.extensions import db
from flask_jwt_extended import JWTManager

def configure_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("app.log")
        ]
    )

def init_postgres(app):
    """Initialize PostgreSQL connection."""
    try:
        db.init_app(app)
        with app.app_context():
            db.engine.connect()
        logging.info("Successfully connected to PostgreSQL")
    except Exception as e:
        logging.error(f"Failed to connect to PostgreSQL: {e}")
        raise e

def init_mongo(app):
    """Initialize MongoDB connection."""
    try:
        # Disconnect any existing connections
        disconnect()
        
        # Connect to MongoDB using settings from app config
        connect(
            db=app.config['MONGODB_SETTINGS']['db'],
            host=app.config['MONGODB_SETTINGS']['host'],
            username=app.config['MONGODB_SETTINGS'].get('username'),
            password=app.config['MONGODB_SETTINGS'].get('password'),
            authentication_source=app.config['MONGODB_SETTINGS'].get('authentication_source', 'admin')
        )
        logging.info("Successfully connected to MongoDB")
    except Exception as e:
        logging.error(f"Failed to connect to MongoDB: {e}")
        raise e

def create_app():
    """Create and configure a Flask application."""
    configure_logging()
    
    # Create Flask app instance with configuration from Config class
    app = Flask(__name__, instance_relative_config=True, static_folder='static')
    
    # Apply configurations from Config class
    app.config.from_object(Config)
    
    # Configure CORS globally
    CORS(app, 
         resources={r"/*": {"origins": "*"}},  # Allow all origins
         supports_credentials=True,
         allow_headers="*",  # Allow all headers
         methods="*"  # Allow all methods
    )
    
    @app.before_request
    def handle_options_request():
        """Handle preflight OPTIONS requests."""
        if request.method == 'OPTIONS':
            response = make_response()
            response.headers.add("Access-Control-Allow-Origin", "*")
            response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
            response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
            response.headers.add("Access-Control-Allow-Credentials", "true")
            return response
    
    # Initialize extensions and databases
    try:
        init_postgres(app)
    except Exception as e:
        logging.error("PostgreSQL initialization failed.")
    
    try:
        init_mongo(app)
    except Exception as e:
        logging.error("MongoDB initialization failed.")
    
    # Initialize JWTManager
    jwt = JWTManager()
    jwt.init_app(app)

    # Register blueprints
    # from app.auth.routes import api as auth_api
    # app.register_blueprint(auth_api, url_prefix='/api')

    return app
