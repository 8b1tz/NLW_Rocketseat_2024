from typing import Dict, List

from sqlalchemy.exc import IntegrityError, NoResultFound

from errors.errors_types.http_conflict import HttpConflictError
from src.models.entities.attendees import Attendees
from src.models.entities.check_in import CheckIns
from src.models.entities.events import Events
from src.models.settings.connection import db_connection_handler


class AttendeesRepository:

    def insert_attendee(self, attendee_info: Dict) -> Dict:
        with db_connection_handler as database:
            try:
                attendee = (
                    Attendees(
                        id=attendee_info['uuid'],
                        name=attendee_info['name'],
                        email=attendee_info['email'],
                        event_id=attendee_info['event_id']
                    )
                )
                database.session.add(attendee)
                database.session.commit()

                return attendee_info
            except IntegrityError:
                raise HttpConflictError('Cadastrante já cadastrado')
            except Exception as exception:
                database.session.rollback()
                raise exception

    def get_attendee_badge_by_id(self, attendee_id: str):
        with db_connection_handler as database:
            try:
                attendee = (
                    database.session
                    .query(Attendees)
                    .join(Events, Events.id == Attendees.event_id)
                    .filter(Attendees.id == attendee_id)
                    .with_entities(
                        Attendees.name,
                        Attendees.email,
                        Events.title
                    )
                    .one()
                )
                return attendee
            except NoResultFound:
                return None

    def get_attendees_by_event_id(self, event_id: str) -> List[Attendees]:
        with db_connection_handler as database:
            attendees = (
                database.session
                .query(Attendees)
                .outerjoin(CheckIns, CheckIns.attendee_id == Attendees.id)
                .filter(Attendees.event_id == event_id)
                .with_entities(
                    Attendees.id,
                    Attendees.name,
                    Attendees.email,
                    CheckIns.created_at.label('checkInAt'),
                    Attendees.create_at.label('createdAt')
                )
                .all()
            )
            return attendees
