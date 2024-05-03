import os
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from database.models import Base, EventParticipants, User
from contextlib import asynccontextmanager

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL)


async def connect_to_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

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
        user = await session.execute(
            select(User).filter(User.discord_id == discord_id)
        )
        return user.scalar_one_or_none()


async def add_user(user_data):
    async with get_session() as session:
        session.add(user_data)
        await session.commit()


async def add_event(event_data):
    async with get_session() as session:
        session.add(event_data)
        await session.commit()


async def remove_participant(user_id, event_id):
    async with get_session() as session:
        participant = await session.execute(
            select(EventParticipants).where(
                user_id == user_id,
                event_id == event_id,
            ).scalar_one_or_none()
        )
        if participant:
            session.delete(participant)
            await session.commit()


async def setup(bot):
    await connect_to_db()
