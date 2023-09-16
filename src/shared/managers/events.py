from typing import List, Optional

from sqlalchemy.orm import Session

from ex_back.models import EventOutbox, EventStore
from ex_back.types import EventStatus, EventType


class OutboxEventManager:
    def __init__(self, session: Session):
        self.session = session

    def save(self, event_type: EventType, event_data: str) -> EventOutbox:
        outbox_event = EventOutbox(event_type=event_type, event_data=event_data)
        self.session.add(outbox_event)
        self.session.commit()
        return outbox_event

    def get_unprocessed_events(self) -> List[EventOutbox]:
        return (
            self.session.query(EventOutbox)
            .filter_by(status=EventStatus.PENDING)
            .with_for_update(skip_locked=True)
            .all()
        )

    def mark_as_processed(self, outbox_event: EventOutbox) -> None:
        outbox_event.status = EventStatus.PUBLISHED
        self.session.add(outbox_event)

    def get_all_events(self) -> List[EventOutbox]:
        return self.session.query(EventOutbox).all()

    def get_event_by_id(self, event_id: int) -> EventOutbox:
        return self.session.query(EventOutbox).filter_by(id=event_id).one_or_none()

    def mark_as_failed(self, outbox_event: EventOutbox, error: str) -> None:
        outbox_event.status = EventStatus.FAILED
        outbox_event.error = error
        self.session.add(outbox_event)


class EventStoreManager:
    def __init__(self, session: Session):
        self.session = session

    def save(self, outbox_event: EventOutbox) -> EventStore:
        """
        Save the event to the append-only event store.
        """
        event = EventStore(
            event_type=outbox_event.event_type,
            event_data=outbox_event.event_data,
            occurred_at=outbox_event.created_at,
            metadata_=outbox_event.metadata_,
        )

        self.session.add(event)
        self.session.commit()
        return event

    def get_event_by_id(self, event_id: int) -> Optional[EventStore]:
        """
        Fetch an event from the event store by its ID.
        """
        return self.session.query(EventStore).filter_by(id=event_id).one_or_none()

    def get_all_events(self) -> List[EventStore]:
        return self.session.query(EventStore).all()
