from typing import Dict

from sqlalchemy.exc import IntegrityError, NoResultFound

from src.errors.errors_types.http_conflict import HttpConflictError
from src.models.entities.attendees import Attendees
from src.models.entities.events import Events
from src.models.settings.connection import db_connection_handler


class EventsRepository:
    def insert_event(self, eventsInfo: Dict) -> Dict:
        with db_connection_handler as database:
            try:
                event = Events(
                    id=eventsInfo['uuid'],
                    title=eventsInfo['title'],
                    slug=eventsInfo['slug'],
                    maximum_attendees=eventsInfo['maximum_attendees'],
                )
                database.session.add(event)
                database.session.commit()

                return eventsInfo
            except IntegrityError:
                raise HttpConflictError("Evento já cadastrado!")
            except Exception as exception:
                database.session.rollback()
                raise exception

    def get_event_by_id(self, event_id: str) -> Events:
        with db_connection_handler as database:
            try:
                event = (
                    database.session
                    .query(Events)
                    .filter(Events.id == event_id)
                    .one()
                )
                return event
            except NoResultFound:
                return None

    def count_event_attendees(self, event_id: str) -> Dict:
        with db_connection_handler as database:
            event_count = (
                database.session
                .query(Events)
                .join(Attendees, Events.id == Attendees.event_id)
                .filter(Events.id == event_id)
                .with_entities(
                    Events.maximum_attendees,
                    Attendees.id
                )
                .all()
            )
            if not event_count:
                return {
                    "maximumAttendees": 0,
                    "attendeesAmount": 0
                }
            return {
                    "maximumAttendees": event_count[0].maximum_attendees,
                    "attendeesAmount": len(event_count)
                }
