from datetime import datetime, timedelta
from app.events.models import Event
from app.extensions import db
from sqlalchemy import func, desc, and_

def get_all_events(filters=None):
    """
    Get all events with optional filtering
    """
    query = Event.query

    if filters:
        # Handle time range filter
        if filters.get('time_range'):
            now = datetime.utcnow()
            if filters['time_range'] == 'day':
                start_date = now - timedelta(days=1)
                query = query.filter(Event.timestamp >= start_date)
            elif filters['time_range'] == 'week':
                start_date = now - timedelta(weeks=1)
                query = query.filter(Event.timestamp >= start_date)
            elif filters['time_range'] == 'month':
                start_date = now - timedelta(days=30)
                query = query.filter(Event.timestamp >= start_date)

        # Handle event type filter - skip if 'all' is selected
        if filters.get('event_type') and filters['event_type'].lower() != 'all':
            query = query.filter(Event.event_type == filters['event_type'])

        # Handle user ID filter
        if filters.get('user_id'):
            query = query.filter(Event.user_id == filters['user_id'])

    # Order by timestamp descending (newest first)
    query = query.order_by(desc(Event.timestamp))

    # Execute query and convert to dict
    events = query.all()
    return [event.to_dict() for event in events]


def get_event_stats(filters=None):
    """
    Get event statistics for visualization
    """
    # query = Event.query

  

    # Get group by parameter (default to day if not specified)
    group_by = filters.get('group_by', 'day') if filters else 'day'

    # Create the grouping expression based on the group_by parameter
    if group_by == 'day':
        group_expr = func.date_trunc('day', Event.timestamp)
    elif group_by == 'week':
        group_expr = func.date_trunc('week', Event.timestamp)
    else:  # month
        group_expr = func.date_trunc('month', Event.timestamp)

    # Group by timestamp and event type, count occurrences
    stats = db.session.query(
        group_expr.label('timestamp'),
        Event.event_type,
        func.count(Event.event_id).label('count')
    ).group_by(
        group_expr,
        Event.event_type
    ).order_by(
        group_expr
    ).all()

    # Format the results
    result = {
        'timestamps': [],
        'event_types': set(),
        'data': {}
    }

    for stat in stats:
        timestamp_str = stat.timestamp.isoformat()
        if timestamp_str not in result['timestamps']:
            result['timestamps'].append(timestamp_str)
        result['event_types'].add(stat.event_type)
        
        if stat.event_type not in result['data']:
            result['data'][stat.event_type] = {}
        result['data'][stat.event_type][timestamp_str] = stat.count

    # Convert event_types set to sorted list
    result['event_types'] = sorted(list(result['event_types']))

    return result 