from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func

from src.models.settings.base import Base


class CheckIns(Base):
    __tablename__ = "check_ins"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=func.now())
    attendee_id = Column(String, ForeignKey("attendees.id"))

    def __repr__(self):
        return f"CheckIns(attendee_id={self.attendee_id})"
