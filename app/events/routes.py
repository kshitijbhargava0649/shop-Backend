import traceback
from flask import request, jsonify
from marshmallow import ValidationError
from flask_restx import Namespace, Resource
from app.events.controller import get_all_events,get_event_stats
from app.events.input_validation import EventFilterSchema
from app.utils.event_logger import log_event

api = Namespace('events', description='Event logging related endpoints')

@api.route('/')
class EventList(Resource):
    def post(self):
        """Create a new event or get events with filters in request body"""
        try:
            data = request.json
            
            # Check if this is a filter request (frontend sends filters in POST body)
            if data and ('event_type' in data or 'user_id' in data or 'time_range' in data):
                # This is a filter request
                filters = data
                
                # Set default time range if none provided
                if not filters.get('time_range'):
                    filters['time_range'] = 'day'  # Default to last 24 hours
                
                # Validate filters
                schema = EventFilterSchema()
                validated_filters = schema.load(filters)
                
                # Get filtered events
                events = get_all_events(validated_filters)
                return events, 200
            
            # Otherwise, this is an event creation request
            if not data:
                return {'error': 'No data provided'}, 400

            # Validate required fields
            required_fields = ['event_type', 'user_id', 'product_id']
            if not all(field in data for field in required_fields):
                return {'error': f'Missing required fields: {", ".join(required_fields)}'}, 400

            # Create event using the event logger
            event = log_event(
                event_type=data['event_type'],
                user_id=data['user_id'],
                product_id=data['product_id']
            )

            if event:
                return event.to_dict(), 201
            return {'error': 'Failed to create event'}, 500
        except ValidationError as e:
            return {'error': e.messages}, 400
        except Exception as e:
            print(traceback.format_exc())
            return {'error': str(e)}, 500

@api.route('/stats')
class EventStats(Resource):
    def get(self):
        """Get event statistics for visualization"""
        try:
            # Get filter parameters from query string
            filters = {}
            
            if request.args.get('group_by'):
                filters['group_by'] = request.args.get('group_by')
            
            # Validate filters if any are provided
            if filters:
                schema = EventFilterSchema()
                validated_filters = schema.load(filters)
            else:
                validated_filters = None
            
            # Get event statistics
            stats = get_event_stats(validated_filters)
            return stats, 200
        except ValidationError as e:
            return {'error': e.messages}, 400
        except Exception as e:
            print(traceback.format_exc())
            return {'error': str(e)}, 500

