from typing import Dict

from sqlalchemy.exc import IntegrityError, NoResultFound

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
                raise Exception("Evento já cadastrado!")
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
