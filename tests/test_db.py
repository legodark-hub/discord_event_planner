from contextlib import asynccontextmanager
from datetime import datetime
import os
import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
import database.db as db
from database.models import Base, User, Event, EventParticipants

DATABASE_URL = os.getenv("TEST_DATABASE_URL")

engine = create_async_engine(DATABASE_URL)


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


@pytest.fixture
async def reset_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        return await conn.run_sync(Base.metadata.create_all)

@pytest.fixture
async def set_data(reset_db):
    await reset_db
    discord_id = 123456789
    message1_id = 123456788
    message2_id = 123456789
    participant_id = 123456780
    await db.add_user(get_session(), 123456789)
    await db.add_event(
        get_session(), message1_id, "test", "test", discord_id, datetime.now(), 1
    )
    await db.add_event(
        get_session(), message2_id, "test2", "test2", discord_id, datetime.now(), 1
    )
    await db.add_user(get_session(), 123456780)
    await db.add_participant(get_session(), participant_id, message1_id)
    await db.add_participant(get_session(), participant_id, message2_id)
    return


@pytest.mark.asyncio
async def test_add_user(reset_db):
    await reset_db
    discord_id = 123456789
    await db.add_user(get_session(), discord_id)
    user = await db.get_user_by_id(get_session(), discord_id)
    assert user is not None


@pytest.mark.asyncio
async def test_add_event(reset_db):
    await reset_db
    message_id = 123456789
    name = "test"
    description = "test"
    author_id = 123456789
    time = datetime.now()
    participants_needed = 1
    await db.add_user(get_session(), author_id)
    await db.add_event(
        get_session(),
        message_id,
        name,
        description,
        author_id,
        time,
        participants_needed,
    )
    event = await db.get_event_by_id(get_session(), message_id)
    assert event is not None


@pytest.mark.asyncio
async def test_add_participant(reset_db):
    await reset_db
    discord_id = 123456789
    message_id = 123456789
    participant_id = 123456780
    await db.add_user(get_session(), discord_id)
    await db.add_event(
        get_session(), message_id, "test", "test", discord_id, datetime.now(), 1
    )
    await db.add_user(get_session(), participant_id)
    await db.add_participant(get_session(), participant_id, message_id)
    participant = await db.get_participant(get_session(), participant_id, message_id)
    assert participant is not None


@pytest.mark.asyncio
async def test_get_user_by_id(set_data):
    user_id = 123456789
    await set_data
    user = await db.get_user_by_id(get_session(), user_id)
    assert user is not None


@pytest.mark.asyncio
async def test_get_event_by_id(set_data):
    await set_data
    event_id = 123456788
    event = await db.get_event_by_id(get_session(), event_id)
    assert event is not None


@pytest.mark.asyncio
async def test_get_events_by_author_id(set_data):
    await set_data
    author_id = 123456789
    events = await db.get_events_by_author_id(get_session(), author_id)
    assert len(events) == 2


@pytest.mark.asyncio
async def test_get_events_by_author_id_count(set_data):
    await set_data
    author_id = 123456789
    count = await db.get_events_by_author_id_count(get_session(), author_id)
    assert count == 2


@pytest.mark.asyncio
async def test_get_events_by_participant_id(set_data):
    await set_data
    participant_id = 123456780
    events = await db.get_events_by_participant_id(get_session(), participant_id)
    assert len(events) == 2


@pytest.mark.asyncio
async def test_get_events_by_participant_id_count(set_data):
    await set_data
    participant_id = 123456780
    count = await db.get_events_by_participant_id_count(get_session(), participant_id)
    assert count == 2


@pytest.mark.asyncio
async def test_get_participant(set_data):
    await set_data
    message_id = 123456789
    participant_id = 123456780
    participant = await db.get_participant(get_session(), participant_id, message_id)
    assert participant is not None


@pytest.mark.asyncio
async def test_remove_event(set_data):
    await set_data
    event_id = 123456789
    await db.remove_event(get_session(), event_id)
    event = await db.get_event_by_id(get_session(), event_id)
    assert event is None


@pytest.mark.asyncio
async def test_remove_participant(set_data):
    await set_data
    event_id = 123456789
    participant_id = 123456780
    await db.remove_participant(get_session(), participant_id, event_id)
    participant = await db.get_participant(get_session(), participant_id, event_id)
    assert participant is None
