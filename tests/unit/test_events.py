"""Unit tests for event models."""

from datetime import datetime

from matrix_system.models.events import Event, EventFilter, EventType


class TestEventType:
    """Test cases for EventType enum."""

    def test_event_types(self) -> None:
        """Test that all event types are defined."""
        assert EventType.HEALTH_UPDATE == "health.update"
        assert EventType.PLAN_CREATED == "guardian.plan"
        assert EventType.PLAN_APPROVED == "guardian.approve"
        assert EventType.PLAN_REJECTED == "guardian.reject"


class TestEvent:
    """Test cases for Event model."""

    def test_create_event(self) -> None:
        """Test creating a valid event."""
        event = Event(
            event_type=EventType.PLAN_CREATED,
            app_uid="test-app",
            payload={"action": "test"},
            actor="test-actor",
        )
        assert event.event_type == EventType.PLAN_CREATED
        assert event.app_uid == "test-app"
        assert event.payload == {"action": "test"}
        assert event.actor == "test-actor"

    def test_event_defaults(self) -> None:
        """Test default values for events."""
        event = Event(event_type=EventType.SYSTEM_STARTUP)
        assert event.actor == "system"
        assert event.payload == {}
        assert event.metadata == {}
        assert isinstance(event.timestamp, datetime)

    def test_is_critical(self) -> None:
        """Test is_critical method."""
        critical_event = Event(event_type=EventType.ERROR_DETECTED)
        assert critical_event.is_critical() is True

        normal_event = Event(event_type=EventType.HEALTH_UPDATE)
        assert normal_event.is_critical() is False

    def test_is_success(self) -> None:
        """Test is_success method."""
        success_event = Event(event_type=EventType.PLAN_APPROVED)
        assert success_event.is_success() is True

        failure_event = Event(event_type=EventType.PLAN_REJECTED)
        assert failure_event.is_success() is False


class TestEventFilter:
    """Test cases for EventFilter model."""

    def test_create_filter(self) -> None:
        """Test creating an event filter."""
        filter_obj = EventFilter(
            event_types=[EventType.PLAN_CREATED, EventType.PLAN_APPROVED],
            app_uid="test-app",
            limit=50,
        )
        assert len(filter_obj.event_types) == 2
        assert filter_obj.app_uid == "test-app"
        assert filter_obj.limit == 50

    def test_filter_defaults(self) -> None:
        """Test default filter values."""
        filter_obj = EventFilter()
        assert filter_obj.limit == 100
        assert filter_obj.offset == 0
        assert filter_obj.event_types is None
