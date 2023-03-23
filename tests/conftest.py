from skill.db.models.sa_models import BaseModel
from tests.db.sa_db_settings import engine
import pytest_asyncio


@pytest_asyncio.fixture()
async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)
