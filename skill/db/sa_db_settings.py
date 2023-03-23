from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from skill.db.repos.sa_repo import SARepoConfig

import os


load_dotenv()


# Needed for some developing features
# Should be False when production
DEBUG = os.getenv("BOT_TOKEN") or False

POSTGRES_DRIVER_NAME = os.getenv("POSTGRES_DRIVER_NAME") or "asyncpg"

POSTGRES_DB_NAME = os.getenv("POSTGRES_DB_NAME") or "postgres"

POSTGRES_USERNAME = os.getenv("POSTGRES_USERNAME") or "postgres"

POSTGRES_HOST = os.getenv("POSTGRES_HOST") or "localhost"

POSTGRES_DB_PORT = os.getenv("POSTGRES_DB_PORT") or "5432"

POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD") or "postgres"

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


engine = create_async_engine(DB_URL, echo=False)


async_session = sessionmaker(  # type: ignore
    engine, expire_on_commit=False, class_=AsyncSession  # type: ignore
)

sa_repo_config = SARepoConfig(connection_provider=async_session)
