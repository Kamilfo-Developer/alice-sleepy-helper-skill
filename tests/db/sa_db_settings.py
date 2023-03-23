from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from sqlalchemy import event
from pathlib import Path
from dotenv import load_dotenv

import os

from skill.db.repos.sa_repo import SARepoConfig


load_dotenv()


# Needed for some developing features
# Should be False when production
DEBUG = os.getenv("BOT_TOKEN") or False


DB_PROVIDER = os.getenv("DB_PROVIDER") or "sqlite"


SQLITE_DRIVER_NAME = os.getenv("SQLITE_DRIVER_NAME") or "aiosqlite"

SQLITE_DB_NAME = os.getenv("SQLITE_DB_NAME") or "data.db"

ROOT_DIR = Path(__file__).parent.parent.parent.resolve()

# In case you want to change path to SQLite DB file,
# just change this variable
SQLITE_DB_FILE_PATH = os.getenv("SQLITE_DB_FILE_PATH") or os.path.join(
    ROOT_DIR, f"{SQLITE_DB_NAME}"
)

# URL for your database
DB_URL = f"sqlite+{SQLITE_DRIVER_NAME}:///" + SQLITE_DB_FILE_PATH


engine = create_async_engine(DB_URL, echo=False)


async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession  # type: ignore
)

sa_repo_config = SARepoConfig(connection_provider=async_session)

if DB_PROVIDER == "sqlite":

    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
