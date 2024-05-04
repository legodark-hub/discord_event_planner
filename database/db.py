import os
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncResult
from sqlalchemy.orm import sessionmaker
from database.models import Base, EventParticipants, User, Event
from contextlib import asynccontextmanager

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL)


# async def connect_to_db():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)


def async_session_generator():
    return sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@asynccontextmanager
async def get_session():
    try:
        session = async_session_generator()
        async with session() as session:
            yield session
    except:
        await session.rollback()
        raise
    finally:
        await session.close()


async def get_user_by_id(discord_id):
    async with get_session() as session:
        user = await session.execute(select(User).where(User.discord_id == discord_id))
        return user.scalar_one_or_none()


async def get_event_by_id(message_id):
    async with get_session() as session:
        event = await session.execute(
            select(Event).where(Event.message_id == message_id)
        )
        return event.scalar_one_or_none()


async def get_participant(discord_id, event_id):
    async with get_session() as session:
        participant = await session.execute(
            select(EventParticipants).where(
                EventParticipants.user_id == discord_id,
                EventParticipants.event_id == event_id,
            )
        )
        return participant.scalar_one_or_none()


async def add_user(discord_id):
    async with get_session() as session:
        new_user = User(discord_id=discord_id)
        session.add(new_user)
        await session.commit()


async def add_event(
    message_id, name, description, author_id, time, participants_needed
):
    async with get_session() as session:
        new_event = Event(
            message_id=message_id,
            name=name,
            description=description,
            author_id=author_id,
            time=time,
            participants_needed=participants_needed,
        )
        session.add(new_event)
        await session.commit()


async def add_participant(participant_id, event_id):
    async with get_session() as session:
        new_participant = EventParticipants(
            event_id=event_id, user_id=participant_id
        )
        session.add(new_participant)
        await session.commit()


async def remove_event(message_id):
    async with get_session() as session:
        event = await get_event_by_id(message_id)
        if event:
            await session.delete(event)
            await session.commit()


async def remove_participant(participant_id, event_id):
    async with get_session() as session:
        participant = await get_participant(
            participant_id, event_id    
        )
        if participant:
            await session.delete(participant)
            await session.commit()


# async def setup(bot):
#     await connect_to_db()
