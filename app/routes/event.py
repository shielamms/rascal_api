"""Routes for event-related operations."""
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from app.deps import CurrentUser, SessionDep, get_current_active_admin, get_current_user
from app.models import (
    Event,
    EventBase,
    EventRegisteration,
    EventsPublic,
)

router = APIRouter(prefix="/events", tags=["events"])


@router.post("/", dependencies=[Depends(get_current_active_admin)])
def create_event(new_event: EventBase, session: SessionDep) -> EventBase:
    event = Event.model_validate(new_event)

    session.add(event)
    session.commit()
    session.refresh(event)
    return event


@router.get("/", dependencies=[Depends(get_current_user)], response_model=EventsPublic)
def read_events(
    session: SessionDep, limit: int = 100, offset: int = 0
) -> list[Event]:
    statement = select(Event).where(Event.status == 1)
    events = session.exec(statement.offset(offset).limit(limit)).all()
    return EventsPublic(data=events)


@router.post("/{event_id}/register", dependencies=[Depends(get_current_user)])
def register_for_event(
    event_id: uuid.UUID, session: SessionDep, current_user: CurrentUser
) -> EventRegisteration:
    event = session.get(Event, event_id)

    existing_registration = session.exec(
        select(EventRegisteration).where(
            EventRegisteration.user_id == current_user.id,
            EventRegisteration.event_id == event_id,
        )
    ).first()
    if existing_registration:
        raise HTTPException(
            status_code=400, detail="User already registered for this event"
        )

    registration = EventRegisteration(user_id=current_user.id, event_id=event_id)
    session.add(registration)
    session.commit()
    session.refresh(registration)
    return registration
