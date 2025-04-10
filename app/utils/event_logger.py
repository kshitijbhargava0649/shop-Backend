from app.events.models import Event
from app.extensions import db

def log_event(event_type, user_id, product_id):
    """
    Log an event to the database
    
    Args:
        event_type (str): Type of event (CREATE, UPDATE, DELETE, etc.)
        user_id (str): ID of the user who performed the action
        product_id (str): ID of the product involved
    
    Returns:
        Event: The created event object
    """
    try:
        # Create a new event
        event = Event(
            event_type=event_type,
            user_id=user_id,
            product_id=product_id
        )
        
        # Save to database
        db.session.add(event)
        db.session.commit()
        
        return event
    except Exception as e:
        # Rollback the session in case of any error
        db.session.rollback()
        # Log the error but don't raise it to avoid breaking the main flow
        print(f"Failed to log event: {str(e)}")
        return None 