import json
from typing import Dict, List, Optional
import requests
from flask import current_app
from datetime import datetime
from .models import Product
from app import db
from app.events.models import Event
from flask import request
from datetime import datetime


def log_product_event(event_type, product_id, user_id=None):
        """Log product-related events to PostgreSQL database"""
        try:
            # Get user ID from request context or use default
            if user_id is None:
                # In a real app, this might come from authentication
                user_id = request.headers.get('User-ID', 'system')
            
            # Create new event record
            new_event = Event(
                event_type=event_type,
                user_id=user_id,
                product_id=product_id,
                timestamp=datetime.utcnow()
            )
            # Add and commit to database
            db.session.add(new_event)
            db.session.commit()
            
            return True
        except Exception as e:
            current_app.logger.error(f"Failed to log event: {str(e)}")
            db.session.rollback()
            return False
        