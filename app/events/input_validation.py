from marshmallow import Schema, fields, validate
from datetime import datetime, timedelta

class EventFilterSchema(Schema):
    event_type = fields.String(required=False, allow_none=True, validate=validate.OneOf([
        'CREATE', 'READ', 'UPDATE', 'DELETE'
    ]))
    user_id = fields.String(required=False, allow_none=True)
    time_range = fields.String(required=False, allow_none=True, validate=validate.OneOf(['day', 'week', 'month']))
    # start_date = fields.DateTime(required=False, allow_none=True)
    # end_date = fields.DateTime(required=False, allow_none=True)
    product_id = fields.String(required=False, allow_none=True)
    group_by = fields.String(required=False, allow_none=True, validate=validate.OneOf(['day', 'week', 'month']))
