import sqlalchemy
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    discord_id = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    created_events = relationship("Event", back_populates="author")
    participated_events = relationship("Event", back_populates="participants")

class Event(Base):
    __tablename__ = "events"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    message_id = sqlalchemy.Column(sqlalchemy.String, unique=True)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime)
    name = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)
    author = relationship("User", back_populates="created_events")
    time = sqlalchemy.Column(sqlalchemy.DateTime)
    participants_needed = sqlalchemy.Column(sqlalchemy.Integer)
    participants = relationship("User", back_populates="participated_events")
