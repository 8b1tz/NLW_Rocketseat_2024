import pytest

from src.models.repository.events_repository import EventsRepository
from src.models.settings.connection import db_connection_handler

db_connection_handler.connect_to_db()


@pytest.mark.skip(reason="Novo registro em banco de dados")
def test_insert_event():
    event = {
        "uuid": "meu_uuid",
        "title": "meu_title",
        "slug": "meu_slug",
        "maximum_attendees": 20
    }

    events_repository = EventsRepository()
    response = events_repository.insert_event(event)
    print(response)


def test_get_event_by_id():
    event_id = "meu_uuid"
    event_repository = EventsRepository()
    response = event_repository.get_event_by_id(event_id)
    print(response)
