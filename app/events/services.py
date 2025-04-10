from app.events.models import Event

def log_event(event_type: str, entity_type: str, entity_id: str) -> None:
    """Log an event to the database"""
    event = Event(
        event_type=event_type,
        entity_type=entity_type,
        entity_id=entity_id
    )
    event.save() 