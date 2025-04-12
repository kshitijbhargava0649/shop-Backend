from datetime import datetime
from sqlalchemy import Enum, Index
from app.extensions import db


class Event(db.Model):
    __tablename__ = 'identifier_events'

    event_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_type = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # SUCCESS, FAILURE, WARNING
    product_id = db.Column(db.String(100), nullable=False)
    # Add composite indexes for better query performance
    __table_args__ = (
        Index('idx_events_user_timestamp', user_id, timestamp),
        Index('idx_events_type_timestamp', event_type, timestamp),
        # Index('idx_events_entity_timestamp', entity_type, entity_id, timestamp),
    )

    def to_dict(self):
        return {
            'event_id': self.event_id,
            'event_type': self.event_type,
            'user_id': self.user_id,    
            'product_id': self.product_id,
            'timestamp': self.timestamp.isoformat(),
        } 