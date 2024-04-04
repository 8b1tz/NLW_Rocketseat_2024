import pytest

from src.models.repository.attendees_repository import AttendeesRepository


@pytest.mark.skip(reason="Novo registro em banco de dados")
def test_insert_attendee():
    event_id = "meu_uuid"
    attendees_info = {
        "uuid": "uuid_attendee",
        "name": "attendee name",
        "email": "meu_email@gmail.com",
        "event_id": event_id
    }
    attendees_repository = AttendeesRepository()
    response = attendees_repository.insert_attendee(attendees_info)
    print(response)


@pytest.mark.skip(reason="...")
def test_get_attendee_badge_by_id():
    attendee_id = "uuid_attendee"
    attendees_repository = AttendeesRepository()
    attendee = attendees_repository.get_attendee_badge_by_id(attendee_id)
    print(attendee)
