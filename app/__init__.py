import logging
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from mongoengine import connect, disconnect
from app.config import Config

# Initialize database objects
postgres_db = SQLAlchemy()

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
        postgres_db.init_app(app)
        with app.app_context():
            postgres_db.engine.connect()
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
    
    # Initialize extensions and databases
    CORS(app)
    init_postgres(app)
    init_mongo(app)

    # Register routes dynamically (example placeholder)
    # from .routes import register_routes
    # register_routes(app)

    return app
