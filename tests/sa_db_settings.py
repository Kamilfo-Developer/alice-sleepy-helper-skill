import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from skill.db.repos.sa_repo import SARepoConfig

load_dotenv()


# Needed for some developing features
# Should be False when production
DEBUG = os.getenv("BOT_TOKEN") or False

DB_PROVIDER = os.getenv("TEST_DB_PROVIDER") or "sqlite"

match DB_PROVIDER:
    case "postgres":
        POSTGRES_DRIVER_NAME = (
            os.getenv("TEST_POSTGRES_DRIVER_NAME") or "asyncpg"
        )

        POSTGRES_DB_NAME = os.getenv("TEST_POSTGRES_DB_NAME") or "postgres"

        POSTGRES_USERNAME = os.getenv("TEST_POSTGRES_USERNAME") or "postgres"

        POSTGRES_HOST = os.getenv("TEST_POSTGRES_HOST") or "localhost"

        POSTGRES_DB_PORT = os.getenv("TEST_POSTGRES_PORT") or "5432"

        POSTGRES_PASSWORD = os.getenv("TEST_POSTGRES_PASSWORD") or "postgres"

        if not POSTGRES_PASSWORD:
            raise EnvironmentError(
                "POSTGRES_PASSWORD required if you are using PostgreSQL"
            )

        DB_URL = (
            f"postgresql+{POSTGRES_DRIVER_NAME}://"
            + f"{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}"
            + f"@{POSTGRES_HOST}:{POSTGRES_DB_PORT}"
            + f"/{POSTGRES_DB_NAME}"
        )

    case _:
        SQLITE_DRIVER_NAME = (
            os.getenv("TEST_SQLITE_DRIVER_NAME") or "aiosqlite"
        )

        SQLITE_DB_NAME = os.getenv("TEST_SQLITE_DB_NAME") or "SAMPLEDATA.db"

        ROOT_DIR = Path(__file__).parent.parent.parent.resolve()

        # In case you want to change path to SQLite DB file,
        # just change this variable
        SQLITE_DB_FILE_PATH = os.getenv(
            "TEST_SQLITE_DB_FILE_PATH"
        ) or os.path.join(ROOT_DIR, f"{SQLITE_DB_NAME}")

        # URL for your database
        DB_URL = f"sqlite+{SQLITE_DRIVER_NAME}:///" + SQLITE_DB_FILE_PATH


engine = create_async_engine(DB_URL, echo=False)


async_session = sessionmaker(  # type: ignore
    engine, expire_on_commit=False, class_=AsyncSession  # type: ignore
)

sa_repo_config = SARepoConfig(connection_provider=async_session)


if DB_PROVIDER == "sqlite":

    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
