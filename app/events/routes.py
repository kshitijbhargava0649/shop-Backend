import traceback
from flask import request, jsonify
from marshmallow import ValidationError
from flask_restx import Namespace, Resource
from app.events.controller import get_all_events, get_event_by_id, get_event_stats
from app.events.input_validation import EventFilterSchema
from app.utils.event_logger import log_event

api = Namespace('events', description='Event logging related endpoints')

@api.route('/')
class EventList(Resource):
    def get(self):
        """Get all events with filtering"""
        try:
            # Get filter parameters from query string
            filters = {}
            
            # Only add filters that are actually provided in the request
            if request.args.get('event_type'):
                filters['event_type'] = request.args.get('event_type')
            if request.args.get('user_id'):
                filters['user_id'] = request.args.get('user_id')
            if request.args.get('time_range'):
                filters['time_range'] = request.args.get('time_range')
            if request.args.get('start_date'):
                filters['start_date'] = request.args.get('start_date')
            if request.args.get('end_date'):
                filters['end_date'] = request.args.get('end_date')
            if request.args.get('product_id'):
                filters['product_id'] = request.args.get('product_id')
            
            # Set default time range if none provided
            if not filters.get('time_range') and not (filters.get('start_date') or filters.get('end_date')):
                filters['time_range'] = 'day'  # Default to last 24 hours
            
            # Validate filters if any are provided
            if filters:
                schema = EventFilterSchema()
                validated_filters = schema.load(filters)
                # Handle time range after validation
                validated_filters = schema.handle_time_range(validated_filters)
            else:
                validated_filters = None
            
            # Get filtered events
            events = get_all_events(validated_filters)
            return events, 200
        except ValidationError as e:
            return {'error': e.messages}, 400
        except Exception as e:
            print(traceback.format_exc())
            return {'error': str(e)}, 500

    def post(self):
        """Create a new event or get events with filters in request body"""
        try:
            data = request.json
            
            # Check if this is a filter request (frontend sends filters in POST body)
            if data and ('event_type' in data or 'user_id' in data or 'time_range' in data or 
                         'start_date' in data or 'end_date' in data or 'product_id' in data):
                # This is a filter request
                filters = data
                
                # Set default time range if none provided
                if not filters.get('time_range') and not (filters.get('start_date') or filters.get('end_date')):
                    filters['time_range'] = 'day'  # Default to last 24 hours
                
                # Validate filters
                schema = EventFilterSchema()
                validated_filters = schema.load(filters)
                # Handle time range after validation
                validated_filters = schema.handle_time_range(validated_filters)
                
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
            
            # Only add filters that are actually provided in the request
            if request.args.get('time_range'):
                filters['time_range'] = request.args.get('time_range')
            if request.args.get('start_date'):
                filters['start_date'] = request.args.get('start_date')
            if request.args.get('end_date'):
                filters['end_date'] = request.args.get('end_date')
            if request.args.get('group_by'):
                filters['group_by'] = request.args.get('group_by')
            
            # Set default time range if none provided
            if not filters.get('time_range') and not (filters.get('start_date') or filters.get('end_date')):
                filters['time_range'] = 'day'  # Default to last 24 hours
            
            # Validate filters if any are provided
            if filters:
                schema = EventFilterSchema()
                validated_filters = schema.load(filters)
                # Handle time range after validation
                validated_filters = schema.handle_time_range(validated_filters)
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

@api.route('/<int:event_id>')
class EventResource(Resource):
    def get(self, event_id):
        """Get a specific event by ID"""
        try:
            event = get_event_by_id(event_id)
            if not event:
                return {'error': 'Event not found'}, 404
            return event, 200
        except Exception as e:
            return {'error': str(e)}, 500 