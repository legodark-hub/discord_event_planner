from datetime import datetime
import os
import sqlalchemy
from sqlalchemy.orm import DeclarativeBase, relationship, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    discord_id = mapped_column(sqlalchemy.String, primary_key=True)
    participated_events = relationship("Event", back_populates="participants")


class Event(Base):
    __tablename__ = "events"
    message_id = mapped_column(sqlalchemy.String, primary_key=True, index=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)
    author_id = sqlalchemy.Column(
        sqlalchemy.String, sqlalchemy.ForeignKey("users.discord_id")
    )
    time = sqlalchemy.Column(sqlalchemy.DateTime)
    participants_needed = sqlalchemy.Column(sqlalchemy.Integer)
    add_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now)
    participants = relationship(
        "User", secondary="event_participants", back_populates="participated_events"
    )


class EventParticipants(Base):
    __tablename__ = "event_participants"
    event_id = sqlalchemy.Column(
        sqlalchemy.String, sqlalchemy.ForeignKey("events.message_id"), primary_key=True
    )
    user_id = sqlalchemy.Column(
        sqlalchemy.String, sqlalchemy.ForeignKey("users.discord_id"), primary_key=True
    )
    # event = relationship("Event", back_populates="message_id")
    # user = relationship("User", back_populates="discord_id")
