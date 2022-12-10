import asyncio
import logging
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import async_scoped_session, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

@asynccontextmanager
async def get_session():
    try:
        session = AsyncSessionMaker()
        session.info['task'] = asyncio.current_task()
        session.info['ref-count'] = session.info.get('ref-count', 0) + 1
        logging.debug("Returned database session %d for task %s",
                      id(session),
                      asyncio.current_task().get_name())
        yield session
    finally:
        if session.info['ref-count'] > 0:
            session.info['ref-count'] -= 1


def initialize():
    global AsyncSessionMaker, LocalSessionMaker
    engine = create_async_engine(f"sqlite+aiosqlite:///{BASE_DIR.parent}/db.sqlite3")
    async_session_factory = sessionmaker(engine, class_=AsyncSession)
    AsyncSessionMaker = async_scoped_session(async_session_factory, scopefunc=asyncio.current_task)
    LocalSessionMaker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
