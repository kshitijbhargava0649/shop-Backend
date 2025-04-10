import pytest
from datetime import datetime, timedelta
from app.events.models import Event
from app.events.controller import get_all_events, get_event_by_id, get_event_stats
from app.utils.event_logger import log_event

def test_log_event():
    """Test basic event logging"""
    result = log_event('TEST', 'test_user', 'test_product')
    assert result is True

def test_get_all_events():
    """Test retrieving all events with filtering"""
    # Create some test events
    log_event('CREATE', 'user1', 'product1')
    log_event('UPDATE', 'user1', 'product1')
    log_event('DELETE', 'user2', 'product2')

    # Test without filters
    events = get_all_events()
    assert len(events) >= 3

    # Test with filters
    filters = {
        'event_type': 'CREATE',
        'user_id': 'user1'
    }
    filtered_events = get_all_events(filters)
    assert len(filtered_events) >= 1
    assert all(e['event_type'] == 'CREATE' for e in filtered_events)
    assert all(e['user_id'] == 'user1' for e in filtered_events)

def test_get_event_stats():
    """Test event statistics generation"""
    # Create events with different timestamps
    now = datetime.utcnow()
    for i in range(3):
        log_event('CREATE', 'user1', 'product1')
        log_event('UPDATE', 'user1', 'product1')

    # Test daily stats
    stats = get_event_stats({'group_by': 'day'})
    assert 'timestamps' in stats
    assert 'event_types' in stats
    assert 'data' in stats
    assert len(stats['event_types']) >= 2  # CREATE and UPDATE
    assert all(t in stats['data'] for t in ['CREATE', 'UPDATE'])

def test_get_event_by_id():
    """Test retrieving a specific event"""
    # Create a test event
    log_event('TEST', 'test_user', 'test_product')
    
    # Get all events to find the latest one
    events = get_all_events()
    latest_event = events[0]  # First event is the latest due to ordering
    
    # Test retrieving by ID
    event = get_event_by_id(latest_event['event_id'])
    assert event is not None
    assert event['event_type'] == 'TEST'
    assert event['user_id'] == 'test_user'
    assert event['product_id'] == 'test_product' 