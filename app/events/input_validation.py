from marshmallow import Schema, fields, validate
from datetime import datetime, timedelta

class EventFilterSchema(Schema):
    event_type = fields.String(required=False, allow_none=True, validate=validate.OneOf([
        'CREATE', 'READ', 'UPDATE', 'DELETE', 'LOGIN', 'LOGOUT', 'EXPORT', 'IMPORT', 'ERROR'
    ]))
    user_id = fields.String(required=False, allow_none=True)
    time_range = fields.String(required=False, allow_none=True, validate=validate.OneOf(['day', 'week', 'month']))
    start_date = fields.DateTime(required=False, allow_none=True)
    end_date = fields.DateTime(required=False, allow_none=True)
    product_id = fields.String(required=False, allow_none=True)
    group_by = fields.String(required=False, allow_none=True, validate=validate.OneOf(['day', 'week', 'month']))

    def handle_time_range(self, data):
        """Handle time range parameter and set appropriate start_date"""
        if data.get('time_range'):
            now = datetime.utcnow()
            if data['time_range'] == 'day':
                data['start_date'] = now - timedelta(days=1)
            elif data['time_range'] == 'week':
                data['start_date'] = now - timedelta(days=7)
            elif data['time_range'] == 'month':
                data['start_date'] = now - timedelta(days=30)
            data['end_date'] = now
        return data 